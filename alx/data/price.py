from googlefinance.client import get_price_data
import pandas as pd

class Price:
    def __init__(self, date, exchange, symbol, close=-1.0):
        self.date = date
        self.symbol = symbol
        self.exchange = exchange

        if close < 0.0:
            query = {
                'q': self.symbol.split('.')[0],
                'i': "86400",
                'x': self.exchange,
                'p': "1D"
            }
            df = get_price_data(query)
            self.close = df['Close'].iloc[0]
        else:
            self.close = close

    def save(self, db):
        try:
            db.cursor.callproc('sp_update_price',
                               (self.date, self.symbol, self.close))
        except Exception:
            raise
