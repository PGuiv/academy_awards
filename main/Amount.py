#Or MonetaryValue
import logging

logger = logging.getLogger('root') 
class Amount(object):
    AVAILABLE_CURRENCIES = ['USD', 'GBP']
    CONVERSION_RATES = {
                        'USD': {
                             'GBP' : 0.65
                                }, 
                        'GBP': {
                             'USD': 1.53
                                }
                       }

    def __init__(self, currency, value = 0):
        if currency in self.AVAILABLE_CURRENCIES:
            self.currency = currency
            self.value = value
        
    def __str__(self):
        return "%s%s" % (self.currency, int(self.value))

    def getValueConverted(self, to_currency):
        if to_currency == self.currency:
            return self.value
        elif to_currency in self.AVAILABLE_CURRENCIES:
            logger.debug("Converted with Rate: " + str(self.CONVERSION_RATES[self.currency][to_currency]))
            return self.value * self.CONVERSION_RATES[self.currency][to_currency]
        else:
            logger.warning("The currency %s is not available [%s]", to_currency, ', '.join(self.AVAILABLE_CURRENCIES))
            return 0
