from datetime import datetime
class Data():
    def __init__(self, s):
        s = s.split(",")
        self.date = datetime.strptime(s[0], '%Y/%m/%d').date()
        self.time = datetime.strptime(s[1],"%H:%M").time()
        self.priceBegin = float(s[2])
        self.highestPrice = float(s[3])
        self.lowestPrice = float(s[4])
        self.endPrice = float(s[5])
        self.tradingVolume = float(s[6])
        self.turnover = float(s[7])

    def __str__(self):
        return str(self.date)+" "+str(self.time)