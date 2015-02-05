class Budget:
    prices = [] 

    def __init__(self, price):
        self.prices.append(price)
        
    def __str__(self):
        result = ''
        for price in self.prices:
            result +=  " " + str(price)

        return result

    def addPrice(self, price):
        self.prices.append(price)
