from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import mapper, sessionmaker

# class Security(ALXDatabase):
#     def __init__(self):
#         super().__init__()
#         security = Table('data', self.metadata, autoload=True)
#
#         mapper(security.Security, security)
#
#     def get_all(self):
#         all = self.db.session.query(Security).all()
#         pass
#
#     def get(self, symbol):
#         pass

class Security:
    def __init__(self, type, symbol, isin, description, exchange=None,
                 sector=None):
        self.type = type
        self.symbol = symbol
        self.isin = isin
        self.description = description
        self.exchange = exchange
        self.sector = sector

    def get(self, db):
        try:
            sql = 'select * from security_vw where symbol = "%s"' % \
                  self.symbol
            db.cursor.execute(sql)
            results = db.cursor.fetchone()
        except Exception:
            raise

        if not results:
            return None

        self.type = results[0]
        self.symbol = results[1]
        self.isin = results[2]
        self.description = results[3]
        self.exchange = results[4]
        self.exchange_name = results[5]
        self.sector = results[6]
        if self.sector == "Consumer Non-Cyc":
            self.sector =  "Consumer Non-Cyclicals"

        return self

    def save(self, db):
        try:
            db.cursor.callproc('sp_update_security',
                               (self.type, self.symbol,
                                self.isin,  self.description,
                                self.exchange, self.sector))
            print("call sp_update_security("
                  "'%s', '%s', '%s', '%s', '%s', '%s')" %
                  (self.type, self.symbol, self.isin,
                   self.description, self.exchange, self.sector))
        except Exception:
            raise


