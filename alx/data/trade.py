class Trade:
    def __init__(self, security, date, side, quantity, price, amount,
                 reference = None, fee = 0.0):
        self.security = security
        self.date = date
        self.symbol = self.security.symbol
        self.side = side
        self.quantity = quantity
        self.price = price
        self.value = amount
        self.reference = reference
        self.fee = fee

    def save(self, db):
        cursor = db.cursor

        try:
            cursor.callproc('sp_update_transaction',
                            (self.date, self.reference, self.symbol,
                             self.side, self.quantity, self.price,
                             self.fee, self.value))
        except Exception as e:
            raise
