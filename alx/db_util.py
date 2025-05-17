import mariadb
from alx.app import ALXapp
import re


class ALXdatabase:
    def __init__(self, dbtype: str = 'mysql', user: str = None,
                 password: str = None, host: str = 'localhost', database: str = None,
                 port: int = 3306):
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

    def connect(self) -> mariadb.Cursor:
        """
        Initiates a connection to the database with parameters set
        in `ALXdatabase` instantiation

        :return: The cursor from the connection made in `mariadb.connect`
        with the parameters set in `ALXdatabase`
        """
        try:
            self.connection = mariadb.connect(**self.config)
        except Exception:
            raise

        self.cursor = self.connection.cursor()

        return self.cursor

    def run(self, sql: str) -> list:
        """
        Tidies up the sql string passed, logs the statement to
        `ALXapp.logger` and executes the statement on the
        `ALXdatabase` object.

        If the statement is a *select*, then the result set is
        returned and *None* otherwise

        :param sql: The sql statement to execute.
        :return: If a *select* statement then the result set
        from the call to execute on the`mariadb.Cursor` or
        *None* if an `insert`, `update`, `upsert` or `replace` statement
        """
        # Make the sql pretty for the log
        sql = sql.replace('\n', ' ').strip()
        sql = re.sub(r'\s\s+', ' ', sql)
        sql = sql.replace('( ', '(')
        self.logger.info(sql)

        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.logger.error('SQL execution failed: %s', format(e))
            raise

        if sql.lower().startswith("select"):
            return self.cursor.fetchall()

        return None

    def close(self):
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