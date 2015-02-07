from Amount import Amount

import customLog
logger = customLog.setup_custom_logger('root')

class Budget(object):

    def __init__(self, amount = Amount('USD', 0)):
        logger.debug("INIT BUDGET WITH %s", str(amount))
        self.amounts = []

        self.amounts.append(amount)
        self.main_currency = amount.currency
        
    def __str__(self):
        result = ''
        for amount in self.amounts:
            result +=  " " + str(amount)

        return result
    
    def updateAmount(self, amount):
        old_amount = self.getAmount(amount.currency)
        if old_amount:
            self.amounts.remove(old_amount)
            self.amounts.append(amount)
        else:
            logger.warning("The amount %s could not be found", str(amount))


    def addAmount(self, amount, convert = True):
        logger.debug(amount)
        old_amount = self.getAmount(amount.currency)
        if old_amount:
            logger.debug("Found the old amount")
            self.updateAmount(amount)
        else:
            logger.debug("I append the amount")
            self.amounts.append(amount)

        if amount.value > 0 and convert:
            logger.debug("I will try to update the main amount")
            main_amount = self.getAmount(self.main_currency)
            logger.debug("Main value %s", main_amount.value)
            if main_amount and main_amount.value == 0:
                logger.debug("I update the main amount")
                main_amount = amount.getConvertedAmount(self.main_currency)
                self.updateAmount(main_amount)

    def getAmount(self, currency):

        #Look in the list of amounts 
        for amount in self.amounts:
            if amount.currency == currency:
                return amount

        return 0

    def getConvertedAmount(self, from_currency, to_currency):
        amount = self.getAmount(from_currency)

        if amount:
            return Amount().getConvertedValue(to_currency)
        else:
            return 0
