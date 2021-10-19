class Trade:
    def __init__(self, date, symbol, side, quantity, price, amount,
                 reference = None, fee = 0.0):
        self.date = date
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.price = price
        self.amount = amount
        self.reference = reference
        self.fee = fee

    def save(self, db):
        cursor = db.cursor

        try:
            cursor.callproc('sp_update_transaction',
                            (self.date, self.reference, self.symbol,
                             self.side, self.quantity, self.price,
                             self.fee, self.amount))
        except Exception as e:
            raise
