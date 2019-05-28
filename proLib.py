import pandas as pd
import numpy as np
from datetime import datetime
# from multiprocessing import Process
import os
from multiprocessing import Pool
data_set_path = "D:\pycharm\datamining\dataminingPro\CharacteristicData"
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
    def findSmilar(self,file_name1_list,file_name2,type,limit):
        maxlist = [["0",0,0,0]]*limit
        # print(maxlist)
        df2 = self.handle_file(file_name2)
        for file_name1 in file_name1_list:
            df1 = self.read_csv(data_set_path+"\\"+file_name1)


            list1 = df1[type+3:type+4]
            list2 = df2[type+3:type+4]

            num = 0
            for index in range(0, min(list1.shape[1],list2.shape[1])-1):
                if list1[index].item() == list2[index].item():
                    num += 1
            # print(num/min(list1.shape[1],list2.shape[1]))
            # print(maxlist[4])
            if(num/(min(list1.shape[1],list2.shape[1])) > maxlist[4][1]):
                maxlist.append([file_name1,num/(min(list1.shape[1],list2.shape[1])),num,min(list1.shape[1],list2.shape[1])])
                maxlist.sort(key=lambda x:-1*x[1])
                maxlist = maxlist[0:5]
            # break
        # print(maxlist)
        return maxlist

    def map_reduce(self,func_name,arg):

        pro_num = arg.__len__()
        pool = Pool(pro_num)
        res_l = []
        for i in range(pro_num):
            # p = Process(target=func_name, args=(arg))
            # process_pool.append(p)
            # p.start()
            res = pool.apply_async(func_name, args=(arg[i]))  # apply_sync的结果就是异步获取func的返回值

            res_l.append(res)  # 从异步提交任务获取结果

        # for res in res_l:  print(res.get())  # 等着func的计算结果
        return res_l
    def get_most_similar(self,stock_id, limit=5):
        file_list = os.listdir(data_set_path)
        func_name = self.findSmilar
        p = int(file_list.__len__()/5)
        arg = [(file_list[0:p], stock_id, 1, limit),
               (file_list[p + 1:2 * p], stock_id, 1,limit,),
               (file_list[2 * p + 1:3 * p], stock_id, 1,limit,),
               (file_list[3 * p + 1:4 * p], stock_id, 1,limit,),
               (file_list[4 * p + 1:5 * p], stock_id, 1,limit,),]
        # print(arg[0])
        result_list = self.map_reduce(func_name, arg)
        # print(result_list[0].get())
        # print(result_list[0].get())
        for i in result_list:
            print(i.get(),"*")


if __name__ == '__main__':
    import time
    b = time.time()
    lib = proLib()
    # df1 = lib.handle_file("D:\data\Stk_1F_2015\SH000001.csv")
    # lib.findSmilar(["SH000001.csv"],df1,1,5)
    lib.get_most_similar("D:\data\Stk_1F_2015\SH000001.csv",limit=5)
    print(time.time()-b)
    # func_name = lib.findSmilar
    # #参数的长度等于线程的个数，建议不超过五个
    # arg = [("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv","D:\data\Stk_1F_2015\SH000001.csv",1),
    #        ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
    #        ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
    #        ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv", 1),
    #        ("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv", "D:\data\Stk_1F_2015\SH000001.csv",1)]
    # result_list = lib.map_reduce(func_name,arg)
    # for i in result_list:
    #     print(i.get())

    # lib.findSmilar("D:\pycharm\datamining\dataminingPro\CharacteristicData\SH000001.csv","D:\data\Stk_1F_2015\SH000001.csv",0)