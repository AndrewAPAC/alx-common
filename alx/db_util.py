from mysql.connector import MySQLConnection
from .app import logger
import re

class ALXDatabase:
    def __init__(self, dbtype='mysql', user=None, passwd=None, host=None,
                 database=None, port=None):
        if dbtype == 'mysql':
            if not port:
                port = 3306
            self.config = {'user': user, 'password': passwd,
                           'host': host, 'database': database,
                           'port': port}
            self.cursor = None
            self.connection = None
        else:
            raise NotImplementedError

    def connect(self):
        try:
            self.connection = MySQLConnection(**self.config)
        except:
            raise

        self.cursor = self.connection.cursor()

        return self.cursor

    def run(self, sql):
        # Make the sql pretty for the log
        sql = sql.replace("\n", " ").strip()
        sql = re.sub("\s\s+", " ", sql)
        sql = sql.replace("( ", "(")
        logger.info(sql)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            logger.error('SQL execution failed: %s', format(e))
            raise

        if sql.lower().startswith("select"):
            return self.cursor.fetchall()

        return None

    def close(self):
        self.connection.close()
        if self.cursor:
            self.cursor.close()
        self.cursor = None
