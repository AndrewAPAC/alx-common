from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import mapper, sessionmaker
from alx.db import ALXDatabase


class Security(ALXDatabase):
    def __init__(self):
        super().__init__()
        security = Table('data', self.metadata, autoload=True)

        mapper(security.Security, security)

    def get_all(self):
        all = self.db.session.query(Security).all()
        pass

    def get(self, symbol):
        pass

