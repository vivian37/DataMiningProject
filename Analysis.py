import dataminingPro.Data as Format
from datetime import datetime
class Analysis():
    def __init__(self):
        print()
    def findSimilar(self,standDataFileName,normalDataFileName):
        f1 =  open(standDataFileName)
        f2 = open(normalDataFileName)
        line1 = f1.readline()
        line2 = f2.readline()
        denominator = 0
        molecular = 0
        lastEndPrice1 = self.findEndPrice(f1,line1)
        lastEndPrice2 = self.findEndPrice(f2,line2)
        while (line1):
            sum1 = self.findEndPrice(f1, line1)
            sum2 = self.findEndPrice(f2, line2)
            # 同增同减就给分子加一
            denominator += 1
            if((sum1 >= lastEndPrice1 and sum2 >= lastEndPrice2) or (sum1 <= lastEndPrice1 and sum2 <= lastEndPrice2) ):
                molecular += 1
            line1 = f1.readline()
            line2 = f2.readline()
        print(molecular,"/",denominator)


    def findEndPrice(self, f, line):
        num = 0
        sum = 0
        while (line):
            f.seek(f.tell())
            result = Format.Data(line)
            if result.time == datetime(2015, 1, 5, 15, 0).time():
                sum += result.endPrice
                num += 1
                if (num == 10):
                    sum = sum / 10
                    return sum
            line = f.readline()
        return sum/num



A = Analysis()
A.findSimilar("D:\data\Stk_1F_2015\SH000001.csv","D:\data\Stk_1F_2015\SH000005.csv")