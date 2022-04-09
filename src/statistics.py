import math
class Statistics:
    def mean(stock):
        return (sum(stock)/len(stock))
    def variance(stock):
        c = sum(stock)/len(stock)
        v=0
        for x in stock:
            v += (x - c)**2
        var=v/(len(stock))
        return var
    def std(stock):
        c = sum(stock)/len(stock)
        v=0
        for x in stock:
            v += (x - c)**2
        var=v/(len(stock))
        return math.sqrt(var)