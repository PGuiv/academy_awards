#Or MonetaryValue
class Amount(object):
    AVAILABLE_CURRENCIES = ['USD', 'GBP']

    def __init__(self, currency, value = 0):
        if currency in self.AVAILABLE_CURRENCIES:
            self.currency = currency
            self.value = value
        
    def __str__(self):
        return "%s%s" % (self.currency, int(self.value))
