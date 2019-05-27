import pandas as pd
import numpy as np
from datetime import datetime
# from multiprocessing import Process
from multiprocessing import Pool
class proLib():
    def __init__(self):
        pass

    def read_csv(self,file_name):
        df = pd.read_csv(file_name,names=(range(-1,365)))
        df = df.dropna(axis=1)
        return df

    def getFeatureList(self, l):

        result = []
        result.append(0)
        for index in range(1, l.shape[1]):

            if l[index].item() > l[index - 1].item():
                result.append(1)
            elif l[index].item() < l[index - 1].item():
                result.append(-1)
            else:
                result.append(0)
        return result

    def handle_file(self,file_name):
        df = pd.read_csv(file_name, names=(
            'Date', 'Time', "beginPrice", "highestPrice", "lowestPrice", "endPrice", "tradingVolume", "turnover"))
        df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d")
        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M")
        df['beginPrice'] = df['beginPrice'].astype(np.int32)
        df['endPrice'] = df['endPrice'].astype(np.int32)
        df['lowestPrice'] = df['lowestPrice'].astype(np.int32)
        df['highestPrice'] = df['highestPrice'].astype(np.int64)
        d = pd.DataFrame()
        d = d.append(df.loc[df['Time'] == datetime(1900, 1, 1, 15, 0)]["endPrice"].reset_index(drop=True))
        d = d.append(df.loc[df['Time'] == datetime(1900, 1, 1, 9, 31)]["beginPrice"].reset_index(drop=True))
        d = d.append(df.groupby("Date").max()["highestPrice"].reset_index(drop=True))
        d = d.append(df.groupby("Date").min()["lowestPrice"].reset_index(drop=True))
        r = []
        r.append(self.getFeatureList(d[0:1]))
        r.append(self.getFeatureList(d[1:2]))
        r.append(self.getFeatureList(d[2:3]))
        r.append(self.getFeatureList(d[3:4]))
        d = d.append(r)
        return d

    #type :0,1,2,3
    def findSmilar(self,file_name1,file_name2,type):
        df1 = self.read_csv(file_name1)
        df2 = self.handle_file(file_name2)

        list1 = df1[type+3:type+4]
        list2 = df2[type+3:type+4]
        num = 0
        for index in range(0, min(list1.shape[1],list2.shape[1])):
            if list1[index].item() == list2[index].item():
                num += 1
        return num,min(list1.shape[1],list2.shape[1])

    def map_reduce(self,func_name,arg):
        pro_num = arg.__len__()
        pool = Pool(pro_num)
        res_l = []
        for i in range(pro_num):
            # p = Process(target=func_name, args=(arg))
            # process_pool.append(p)
            # p.start()
            res = pool.apply_async(func_name, args=(arg[1]))  # apply_sync的结果就是异步获取func的返回值
            res_l.append(res)  # 从异步提交任务获取结果

        # for res in res_l:  print(res.get())  # 等着func的计算结果
        return res_l
if __name__ == '__main__':
    lib = proLib()
    func_name = lib.findSmilar
    #参数的长度等于线程的个数，建议不超过五个
    arg = [("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv","D:\data\Stk_1F_2015\SH000001.csv",1),
           ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
           ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
           ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
           ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv",1)]
    result_list = lib.map_reduce(func_name,arg)
    for i in result_list:
        print(i.get())

    # lib.findSmilar("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv","D:\data\Stk_1F_2015\SH000001.csv",0)