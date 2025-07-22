import mariadb
from alx.app import ALXapp
import re
from sql_formatter.core import format_sql


class ALXdatabase:
    def __init__(self, dbtype: str = 'mysql', user: str = None,
                 password: str = None, host: str = 'localhost', database: str = None,
                 port: int = 3306, autoconnect: bool = False) -> None:
        """
        Simplifies and removes repetitive statements to connect to a database.

        :param dbtype: The database type.  Default is *mysql* and is the
        only supported type at present. Note that mysql is a synonym for
        mariadb
        :param user: The username to use
        :param password: The password to use
        :param host: The host to connect (default is `localhost`)
        :param database: The name of the database
        :param port: The port (default is mariadb, 3306)
        :param autoconnect: If True then connect to the database after
         initialisation. Default is False
        """

        self.logger = ALXapp.logger
        """The default logger from the alx.app.ALXapp.logger"""
        self.cursor = None
        """The cursor assigned in `ALXdatabase.connect` after
        making the database connection"""
        self.connection = None
        """The connection assigned in `ALXDatabase.connect` after
        making the database connection"""
        if dbtype == 'mysql':
            self.config = {'user': user, 'password': password,
                           'host': host, 'database': database,
                           'port': port}
            self.cursor = None
            self.connection = None
        else:
            raise NotImplementedError
        self.logger.info("Initialising database connection to %s on %s as %s",
                         self.config['database'], self.config['host'],
                         self.config['user'])

        if autoconnect:
            self.connect()

    def connect(self) -> mariadb.Cursor:
        """
        Initiates a connection to the database with parameters set
        in `ALXdatabase` instantiation

        :return: The cursor from the connection made in `mariadb.connect`
        with the parameters set in `ALXdatabase`
        """
        try:
            self.connection = mariadb.connect(**self.config)
            self.logger.info("Connected to %s database on %s as %s",
                             self.config['database'], self.config['host'],
                             self.config['user'])
        except Exception:
            raise

        self.cursor = self.connection.cursor()

        return self.cursor

    def run(self, sql: str, name: str = None,
            params: tuple | list | dict = None,
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
        from the call to execute on the`mariadb.Cursor` or
        *None* if an `insert`, `update`, `upsert` or `replace` statement
        """
        sql = sql.strip()   # remove any extra whitespace from string boundaries

        if name:
            log = name + ":\n" + format_sql(sql)
        else:
            log = "\n" + format_sql(sql)

        # Write the SQL on a new line for easy cut & paste
        self.logger.info(log)

        try:
            if multi and params:
                self.cursor.executemany(sql, params)
            elif params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
        except Exception as e:
            self.logger.error('SQL execution failed: %s', format(e))
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
        except mariadb.ProgrammingError:
            pass

        self.cursor = None
        self.connection = None

    def __enter__(self) -> None:
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
        except Exception:
            pass