
class Position:
    def __init__(self, date, account, symbol, position=0, close=0.0):
        self.date = date
        self.account = account
        self.symbol = symbol
        self.position = position
        self.close = close

    def save(self, db):
        cursor = db.cursor

        try:
            # TODO: If securuity doesx not exist, need to add it.
            # Do in stored proc?
            # Could also save the price in here?
            cursor.callproc('sp_update_position',
                            (self.date, self.symbol, self.account,
                             int(self.position)))
        except Exception:
            raise
