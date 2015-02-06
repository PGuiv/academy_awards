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
            result +=  " " + str(amount)

        return result

    def addAmount(self, amount):
        self.amounts.append(amount)
