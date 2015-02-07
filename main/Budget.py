class Budget(object):

    def __init__(self, amounts):
        self.amounts = []

        if isinstance(amounts, list):
            for amount in amounts:
                self.amounts.append(amount)
        else:
            self.amounts.append(amounts)

        
    def __str__(self):
        result = ''
        for amount in self.amounts:
            result +=  " " + str(self.getAmount(amount))

        return result

    def addAmount(self, amount):
        self.amounts.append(amount)

    def getAmount(self, currency, convert = True):

        #Look in the list of amounts 
        for amount in self.amounts:
            if amount.currency == currency:
                if amount.value == 0 && convert:
                    for amount in self.amounts:
                        if amount.value != 0:
                            self.getConvertedAmount(amount.currency, currency)

                return amount


        return 0

    def getConvertedAmount(self, from_currency, to_currency):
        amount = self.getAmount(from_currency)

        if amount:
            return Amount().getConvertedValue(to_currency)
        else:
            return 0
        
