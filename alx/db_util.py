# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
# Provides ALXdatabase class for executing SQL queries on MariaDB/MySQL,
# PostgreSQL, and SQLite backends using a consistent API.
#
from alx.app import ALXapp
import re
from typing import Any
from alx.strings import normalize
from sql_formatter.core import format_sql
# Only want to support modules that are installed.
try:
    import psycopg2
    has_postgres = True
except ImportError:
    psycopg2 = None
    has_postgres = False
try:
    import sqlite3
    has_sqlite = True
except ImportError:
    sqlite3 = None
    has_sqlite = False  # basically always True, part of stdlib
try:
    import mariadb as mysql
    has_mysql = True
except ImportError:
    try:
        import pymysql as mysql
        has_mysql = True
    except ImportError:
        has_mysql = False
        mysql = None


class ALXdatabase:
    def __init__(self, dbtype: str = 'mysql', user: str = None,
                 password: str = None, host: str = 'localhost', database: str = None,
                 port: int = 3306, autoconnect: bool = False,
                 autocommit: bool = False) -> None:
        """
        Simplifies and removes repetitive statements to connect to a database.

        :param dbtype: The database type.  Default is *mysql* which can also
         be used for *mariadb*. Supported options are
           * `mysql` -> `pip install pymysql`
           * `mariadb` -> `pip install mariadb`
           * `postgres` -> `pip install psycopg2`
           * `sqlite`
        :param user: The username to use
        :param password: The password to use
        :param host: The host to connect (default is `localhost`)
        :param database: The name of the database
        :param port: The port (default is mariadb, 3306)
        :param autoconnect: If True then connect to the database after
            initialisation. Default is False
        :param autocommit: If True then execute `commit` after each
            successful transaction

        You can also do this:
        ```
        with ALXdatabase(dbtype='sqlite', database=':memory:', autoconnect=True) as db:
            db.run("CREATE TABLE test (id INT)")
            db.run("INSERT INTO test (id) VALUES (1)")
        # <-- commits automatically, or rolls back if an error occurred
        ```
        """

        self.logger = ALXapp.logger
        """The default logger from the alx.app.ALXapp.logger. This class needs
        to be used so the logger is initialised"""
        self.cursor = None
        """The cursor assigned in `ALXdatabase.connect` after
        making the database connection"""
        self.connection = None
        """The connection assigned in `ALXdatabase.connect` after
        making the database connection"""
        self.autocommit = autocommit
        """Whether to automatically commit a successful transaction"""

        dbtype = normalize(dbtype)

        if dbtype == 'mariadb':
            self.dbtype = 'mysql'
        else:
            self.dbtype = dbtype

        self._params = {'user': user, 'password': password,
                        'host': host, 'database': database,
                        'port': port}
        if self.dbtype == 'sqlite':
            self._params['database'] = database or ':memory:'

        self.logger.info("Initialising %s database connection to %s on %s as %s",
                         dbtype, self._params['database'], self._params['host'],
                         self._params['user'])

        if autoconnect:
            self.connect()

    def connect(self) -> Any:
        """
        Initiates a connection to the database with parameters set
        in `ALXdatabase` constructor

        :return: The cursor from the connection made in `mariadb.connect`
        with the parameters set in `ALXdatabase`
        """
        try:
            if self.dbtype == 'mysql':
                if not has_mysql:
                    raise RuntimeError("MySQL/MariaDB support not available")
                self.connection = mysql.connect(**self._params)
            elif self.dbtype == 'postgres':
                if not has_postgres:
                    raise RuntimeError("PostgreSQL support not available")
                self.connection = psycopg2.connect(**self._params)
            elif self.dbtype == 'sqlite':
                if not has_sqlite:
                    raise RuntimeError("SQLite support not available")
                self.connection = sqlite3.connect(self._params['database'])
            else:
                raise ValueError(f"Unsupported database type: {self.dbtype}")
        except Exception as e:
            self.logger.error("Connection failed: %s", format(e))

        self.cursor = self.connection.cursor()
        self.logger.info("Connected successfully")
        return self.cursor

    def _convert_placeholders(self, sql: str) -> str:
        if self.dbtype == 'sqlite':
            return re.sub(r'%s', '?', sql)
        return sql

    def run(self, sql: str, name: str = None,
            params=None,
            multi: bool = False) -> list:
        """
        Tidies up the SQL string passed, logs the statement to
        `ALXapp.logger` and executes the statement on the
        `ALXdatabase` object.

        Supports parameterized queries using the DB-API parameter
        style (? or %s).

        If the statement is a *select*, then the result set is
        returned and *None* otherwise

        :param sql: The SQL statement to execute.
        :param name: Optionally name the query to identify it in the log
        :param params: A tuple or list of parameters to use with the SQL query.
        :param multi: If True, use executemany() for bulk inserts.

        :return: If a *select* statement then the result set
        from the call to execute on the `cursor` or
        an empty list if an `insert`, `update`, `upsert` or
        `replace` statement
        """
        sql = sql.strip()
        sql = self._convert_placeholders(sql)

        if name:
            log = "%s:\n%s" % (name, format_sql(sql))
        else:
            log = format_sql(sql)
        self.logger.debug(log)

        try:
            if multi and params:
                self.cursor.executemany(sql, params)
            elif params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            if self.autocommit:
                try:
                    self.connection.commit()
                except Exception as e:
                    self.logger.warning("Autocommit failed: %s", e)
        except Exception as e:
            self.logger.error('SQL execution failed: %s', e)
            raise

        if sql.lower().startswith("select"):
            self.logger.info("%d rows returned", self.cursor.rowcount)
            return self.cursor.fetchall()

        self.logger.info("%d rows affected", self.cursor.rowcount)
        return []

    def commit(self):
        """
        Commit the current transaction.  This function should be called
        after modifying or inserting data. It is not done automatically
        to allow for exception handling

        :return: None
        """
        self.connection.commit()

    def rollback(self):
        """
        Rollback the current transaction. Do not commit the outstanding
        data. It is not done automatically to allow for exception handling

        :return: None
        """
        self.connection.rollback()

    def close(self) -> None:
        """
        Close the `ALXdatabase` connection and cursor and
        set them to None
        """
        try:
            if self.connection:
                self.connection.close()
            if self.cursor:
                self.cursor.close()
        except (sqlite3.Error, Exception):
            pass

        self.cursor = None
        self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()

    def __del__(self):
        try:
            self.close()
        except (sqlite3.Error, Exception):
            pass
