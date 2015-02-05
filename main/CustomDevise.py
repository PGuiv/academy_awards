class CustomDevise:
    AVAILABLE_CURRENCIES = ['USD', 'GBP']
    currency = ''
    value = ''

    def __init__(self, currency, value):
        if currency in self.AVAILABLE_CURRENCIES:
            self.currency = currency
            self.value = value
        
    def __str__(self):
        return "%s%s" % (self.currency, self.value)
