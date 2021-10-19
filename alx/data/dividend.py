# Dividend Class
#
# Author: andrew lister
# Date: Oct 2021

class Dividend:
    def __init__(self, paydate, symbol, quantity, divpershare, total,
                 franked = 0, unfranked = 0, credit = 0):
        self.paydate = paydate
        self.symbol = symbol
        self.quantity = quantity
        self.divpershare = divpershare
        self.total = total
        self.franked = franked
        self.unfranked = unfranked
        self.credit = credit

    def save(self, db):
        cursor = db.cursor

        try:
            cursor.callproc('sp_update_dividend',
                            (self.paydate, self.symbol,
                            'F', self.divpershare, self.franked,
                            self.unfranked, self.credit, self.total))
        except Exception as e:
            raise

