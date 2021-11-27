
class Position:
    def __init__(self, security, date, account, position=0, close=0.0):
        self.security = security
        self.date = date
        self.account = account
        self.symbol = security.symbol
        self.value = position
        self.close = close

    def save(self, db):
        cursor = db.cursor

        try:
            # TODO: If security does not exist, need to add it.
            # Do in stored proc?
            # Could also save the price in here?
            cursor.callproc('sp_update_position',
                            (self.date, self.symbol, self.account,
                             int(self.value)))
        except Exception:
            raise
