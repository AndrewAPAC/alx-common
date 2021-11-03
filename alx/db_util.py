from mysql.connector import MySQLConnection
#from sqlalchemy import create_engine, MetaData, Table
#from sqlalchemy.orm import mapper, sessionmaker


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


    def close(self):
        self.connection.close()
        self.cursor.close()
        self.cursor = None
