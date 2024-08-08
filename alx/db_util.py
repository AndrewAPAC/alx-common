from mysql.connector import MySQLConnection
from .app import logger

class ALXDatabase:
    def __init__(self, type='mysql', user=None, passwd=None, host=None,
                 database=None):
        self.config = {'user': user, 'password': passwd,
                       'host': host, 'database': database}
        self.cursor = None

    def connect(self):
        try:
            self.connection = MySQLConnection(**self.config)
        except:
            raise

        self.cursor = self.connection.cursor()

        return self.cursor

    def run(self, sql):
        sql = sql.replace('\n', ' ').strip()
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
