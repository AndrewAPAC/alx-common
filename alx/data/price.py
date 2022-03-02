#from googlefinance.client import get_price_data
#import pandas as pd

class Price:
    def __init__(self, security, date, close=-1.0):
        self.security = security
        self.date = date
        self.symbol = security.symbol
        self.value = close

    def save(self, db):
        try:
            db.cursor.callproc('sp_update_price',
                               (self.date, self.symbol, self.value))
        except Exception:
            raise
