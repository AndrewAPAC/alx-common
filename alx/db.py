from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from alx.misc import singleton
from alx.app import logger as logging

# @singleton
class ALXDatabase:
    def __init__(self, type=None, user=None, passwd=None,
                 host=None, database=None, debug=False):
        connectstr = "%s://%s:%s@%s/%s" % \
                     (type, user, passwd, host, database)
        logging.debug("Connecting to {}:{} as {}".format(host, database, user))

        self.engine = create_engine(connectstr,
                                    echo=debug,
                                    pool_pre_ping=True)

        self.metadata = MetaData(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

