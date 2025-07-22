import pytest
from unittest.mock import MagicMock, call
from alx.db_util import ALXdatabase  # Adjust import as needed

@pytest.fixture
def mock_db_util():
    db = ALXdatabase.__new__(ALXdatabase)  # bypass __init__ to set attributes manually
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
    mock_db_util.logger.info.assert_any_call("%d rows returned", 2)

def test_run_insert_returns_empty_list(mock_db_util):
    mock_db_util.cursor.execute.return_value = None
    mock_db_util.cursor.rowcount = 1

    sql = "INSERT INTO test_table VALUES (1, 'x')"
    result = mock_db_util.run(sql, name="insert_test")

    assert result == []
    mock_db_util.cursor.execute.assert_called_once_with(sql)
    mock_db_util.logger.info.assert_any_call("%d rows affected", 1)

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
