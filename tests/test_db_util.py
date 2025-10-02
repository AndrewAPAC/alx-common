# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# pytest routines for alx.db_util

import pytest
from unittest.mock import MagicMock, call
from alx.db_util import ALXdatabase  # Adjust import as needed


@pytest.fixture
def mock_db_util():
    db = ALXdatabase(dbtype="sqlite", database=":memory:", autoconnect=False)
    db.connection = MagicMock()
    db.cursor = MagicMock()
    db.logger = MagicMock()
    return db


def test_run_select_returns_results(mock_db_util):
    mock_db_util.cursor.execute.return_value = None
    mock_db_util.cursor.fetchall.return_value = [('a', 1), ('b', 2)]
    mock_db_util.cursor.rowcount = 2

    sql = "SELECT * FROM test_table"
    result = mock_db_util.run(sql, name="select_test")

    assert result == [('a', 1), ('b', 2)]
    mock_db_util.cursor.execute.assert_called_once_with(sql)
    mock_db_util.logger.debug.assert_any_call("%d rows returned", 2)


def test_run_insert_returns_empty_list(mock_db_util):
    mock_db_util.cursor.execute.return_value = None
    mock_db_util.cursor.rowcount = 1

    sql = "INSERT INTO test_table VALUES (1, 'x')"
    result = mock_db_util.run(sql, name="insert_test")

    assert result == []
    mock_db_util.cursor.execute.assert_called_once_with(sql)
    mock_db_util.logger.debug.assert_any_call("%d rows affected", 1)


def test_run_logs_sql_formatting(mock_db_util):
    sql = "  SELECT * FROM test_table "
    formatted_sql = "SELECT * FROM test_table"

    mock_db_util.cursor.execute.return_value = None
    mock_db_util.cursor.fetchall.return_value = []
    mock_db_util.cursor.rowcount = 0

    mock_db_util.run(sql, name="formatted_test")

    # This checks that whitespace is stripped
    call_args = mock_db_util.cursor.execute.call_args[0][0]
    assert call_args == formatted_sql


def test_run_raises_exception_on_failure(mock_db_util):
    sql = "SELECT * FROM missing_table"
    mock_db_util.cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        mock_db_util.run(sql, name="error_test")

    mock_db_util.logger.error.assert_called_once()


def test_run_with_params(mock_db_util):
    sql = "SELECT * FROM test_table WHERE id = %s"
    mock_db_util.dbtype = "sqlite"  # ensure placeholder conversion applies
    mock_db_util.cursor.fetchall.return_value = [(1,)]
    mock_db_util.cursor.rowcount = 1

    result = mock_db_util.run(sql, params=(1,), name="param_test")

    expected_sql = "SELECT * FROM test_table WHERE id = ?"
    assert result == [(1,)]
    mock_db_util.cursor.execute.assert_called_once_with(expected_sql, (1,))


def test_run_with_executemany(mock_db_util):
    sql = "INSERT INTO test_table (id) VALUES (%s)"
    mock_db_util.cursor.rowcount = 2
    params = [(1,), (2,)]

    result = mock_db_util.run(sql, params=params, multi=True, name="bulk_insert")

    assert result == []
    expected_sql = "INSERT INTO test_table (id) VALUES (?)"
    mock_db_util.cursor.executemany.assert_called_once_with(expected_sql, params)


def test_sqlite_placeholder_conversion():
    db = ALXdatabase.__new__(ALXdatabase)
    db.dbtype = 'sqlite'

    original_sql = "SELECT * FROM table WHERE id = %s AND name = %s"
    expected_sql = "SELECT * FROM table WHERE id = ? AND name = ?"

    assert db._convert_placeholders(original_sql) == expected_sql


def test_context_manager_commit(monkeypatch):
    db = ALXdatabase.__new__(ALXdatabase)
    db.commit = MagicMock()
    db.rollback = MagicMock()
    db.close = MagicMock()

    with db:
        pass

    db.commit.assert_called_once()
    db.rollback.assert_not_called()
    db.close.assert_called_once()


def test_context_manager_rollback_on_exception(monkeypatch):
    db = ALXdatabase.__new__(ALXdatabase)
    db.commit = MagicMock()
    db.rollback = MagicMock()
    db.close = MagicMock()

    try:
        with db:
            raise ValueError("Fail inside context")
    except ValueError:
        pass

    db.rollback.assert_called_once()
    db.commit.assert_not_called()
    db.close.assert_called_once()


@pytest.fixture
def sqlite_db(tmp_path):
    dbfile = tmp_path / "test.sqlite"
    db = ALXdatabase(dbtype="sqlite", database=str(dbfile), autoconnect=True)
    yield db
    db.close()


def test_sqlite_create_table(sqlite_db):
    sqlite_db.run("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """, name="create_users")

    result = sqlite_db.run("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert result == [('users',)]


def test_sqlite_insert_and_select(sqlite_db):
    sqlite_db.run("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)", name="create_items")
    sqlite_db.run("INSERT INTO items (name) VALUES (%s)", params=("Widget",), name="insert_item")

    rows = sqlite_db.run("SELECT id, name FROM items", name="select_items")
    assert len(rows) == 1
    assert rows[0][1] == "Widget"


def test_sqlite_bulk_insert(sqlite_db):
    sqlite_db.run("CREATE TABLE log (msg TEXT)", name="create_log")
    messages = [("Log 1",), ("Log 2",), ("Log 3",)]
    sqlite_db.run("INSERT INTO log (msg) VALUES (%s)", params=messages, multi=True)

    results = sqlite_db.run("SELECT msg FROM log")
    assert [r[0] for r in results] == ["Log 1", "Log 2", "Log 3"]
