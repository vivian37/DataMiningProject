# from multiprocessing import Process
import os
from datetime import datetime
from multiprocessing import Pool

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

data_set_path = "D:\pycharm\datamining\dataminingPro\CharacteristicData"


class proLib():
    def __init__(self):
        pass

    def read_csv(self, file_name):
        df = pd.read_csv(file_name, names=(range(-1, 365)))
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

    def handle_file(self, file_name):
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

    # type :0,1,2,3
    def findSmilar(self, file_name1_list, file_name2, type, limit,maxormin):
        maxlist = [["0", 0, 0, 0]] * limit
        minlist = [["0", 0, 0, 0]] * limit
        # print(maxlist)
        df2 = self.handle_file(file_name2)
        for file_name1 in file_name1_list:
            df1 = self.read_csv(data_set_path + "\\" + file_name1)

            list1 = df1[type + 3:type + 4]
            list2 = df2[type + 3:type + 4]

            num = 0
            num1 = 0
            for index in range(0, min(list1.shape[1], list2.shape[1]) - 1):
                if list1[index].item() == list2[index].item():
                    num += 1
                if list1[index].item() == -1*list2[index].item():
                    num1 += 1
            # print(num/min(list1.shape[1],list2.shape[1]))
            # print(maxlist[4])
            if (num / (min(list1.shape[1], list2.shape[1])) > maxlist[4][1]):
                maxlist.append(
                    [file_name1.split('.')[0], num / (min(list1.shape[1], list2.shape[1])), num,
                     min(list1.shape[1], list2.shape[1])])
                maxlist.sort(key=lambda x: -1 * x[1])
            if (num1 / (min(list1.shape[1], list2.shape[1])) > minlist[4][1]):
                minlist.append(
                    [file_name1.split('.')[0], num1 / (min(list1.shape[1], list2.shape[1])), num1,
                     min(list1.shape[1], list2.shape[1])])
                minlist.sort(key=lambda x: -1 * x[1])
                minlist = minlist[0:5]
            # break
        # print(maxlist)
        if maxormin == 1:
            return maxlist
        else:
            return minlist

    def map_reduce(self, func_name, arg):

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

    def get_most_similar(self, stock_id,limit=5):
        # file_list = os.listdir(data_set_path)
        file_list = []
        with open("correct_file_name","r") as f:
            line = f.readline()[:-1]
            f.seek(f.tell())
            while(line):
                file_list.append(line)
                line = f.readline()[:-1]
                f.seek(f.tell())
        func_name = self.findSmilar
        p = int(file_list.__len__() / 5)
        arg = [(file_list[0:p], stock_id, 1, limit,1),
               (file_list[p + 1:2 * p], stock_id, 1, limit,1),
               (file_list[2 * p + 1:3 * p], stock_id, 1, limit,1),
               (file_list[3 * p + 1:4 * p], stock_id, 1, limit,1),
               (file_list[4 * p + 1:5 * p], stock_id, 1, limit,1), ]
        # print(arg[0])
        result_list = self.map_reduce(func_name, arg)
        # print(result_list)
        # print(result_list[0].get())
        # print(result_list[0].get())
        ret = list()

        for i in result_list:
            ret.extend(i.get())
        ret.sort(key=lambda d: d[1], reverse=True)
        # return ret[:limit]
        print(ret)
        return ret

    def get_most_differ(self, stock_id,limit=5):
        # file_list = os.listdir(data_set_path)
        file_list = []
        with open("correct_file_name","r") as f:
            line = f.readline()[:-1]
            f.seek(f.tell())
            while(line):
                file_list.append(line)
                line = f.readline()[:-1]
                f.seek(f.tell())
        func_name = self.findSmilar
        p = int(file_list.__len__() / 5)
        arg = [(file_list[0:p], stock_id, 1, limit,0),
               (file_list[p + 1:2 * p], stock_id, 1, limit,0),
               (file_list[2 * p + 1:3 * p], stock_id, 1, limit,0),
               (file_list[3 * p + 1:4 * p], stock_id, 1, limit,0),
               (file_list[4 * p + 1:5 * p], stock_id, 1, limit,0), ]
        # print(arg[0])
        result_list = self.map_reduce(func_name, arg)
        # print(result_list)
        # print(result_list[0].get())
        # print(result_list[0].get())
        ret = list()

        for i in result_list:
            ret.extend(i.get())
        ret.sort(key=lambda d: d[1], reverse=True)
        # return ret[:limit]
        print(ret)
        return ret

    def _get_freq_item_stock_set(self):
        rule_dic = []
        with open("freq_item_stock_set","r") as f:

            line = f.readline()
            f.seek(f.tell())
            while (line):
                s = set()
                content =line.split(":")[1][1:-1].split(",")
                for i in content:
                    s.add(i[2:-3])
                rule_dic.append(s)
                line = f.readline()
                f.seek(f.tell())
        return rule_dic


    def get_rule(self,reson_lit,result_lit):
        rule_dic = self._get_freq_item_stock_set()
        set1 = rule_dic[reson_lit[0]]
        for i in reson_lit[1:]:
            set1 = set1 & rule_dic[i]
        fenmu = set1.__len__()
        print(fenmu)
        for i in result_lit:
            set1 = set1 & rule_dic[i]
        fenzi = set1.__len__()

        set2 = rule_dic[result_lit[0]]
        for i in result_lit:
            set2 = set2 & rule_dic[i]
        print("conf:", fenzi, "/", fenmu)
        print("interest:",set2.__len__(),"/",1355)

    def k_mean(self,k):

        df1 = self.read_csv("correct_file_characterristic1")

        center_lst_index =[]
        for _ in range(k):
            center_lst_index.append([random.randint(0,1354)])

        print(center_lst_index)
        center_lst = []
        for index,item in enumerate(center_lst_index):
            center_lst.append(np.array(df1.iloc[[item[0]]]).tolist())
        for time in range(0,10):
            for i in range(0, 1355):
                t = df1.iloc[[i]]
                result = self._calculate_jcard_distance(center_lst,np.array(t).tolist())
                result.sort(key=lambda x:x[1])
                center_lst_index[result[-1][0]].append(i)
            for idx2,temp_lst in enumerate(center_lst_index):
                xmin= 0
                idxnum = 0
                for idx1,item1 in enumerate(temp_lst):
                    l = np.array(df1.iloc[[idx1]]).tolist()
                    x = 0
                    for item2 in temp_lst[0:idx1]:
                        x1 = self._calculate_jcard_distance([np.array(df1.iloc[[item2]]).tolist()],l)
                        x += x1[0][1]
                    for item2 in temp_lst[idx1+1:]:
                        x2 = self._calculate_jcard_distance([np.array(df1.iloc[[item2]]).tolist()],l)
                        x += x2[0][1]
                    if(x>xmin):
                        xmin = x
                        idxnum = idx1
                # print(idxnum,end=" ")
                # print(xmin,temp_lst[idxnum],"*")
                center_lst_index[idx2] = [temp_lst[idxnum]]
                center_lst = []
                for index, item in enumerate(center_lst_index):
                    center_lst.append(np.array(df1.iloc[[item[0]]]).tolist())
            print(center_lst_index)
            # print(center_lst_index)

    def cluster(self):
        df1 = self.read_csv("correct_file_characterristic1")
        clst = [[127],
[558],
[662],
[691],
[793],
[802],
[834],
[876],
[1019]]
        type = 0
        for i in clst:

            tempDic = dict()
            for x in range(24):
                tempDic[x] = []

            for j in i:
                # print(j)
                l = np.array(df1.iloc[[j]]).tolist()[0]

                for idex in range(0,24):
                    s = 0
                    for ge in range(0,10):
                        indx = idex *10 + ge
                        s += l[indx]
                    if s > 0:
                        tempDic[idex].append(1)
                    else:
                        tempDic[idex].append(-1)
                # for idex,item in enumerate(l):
                #     if idex< 30:
                #         tempDic[idex].append(item)
            # for y in tempDic:
            #     print(tempDic[y])
            tf = pd.DataFrame(tempDic)
            parallel_coordinates(tf,0,color="red")
            plt.savefig("myresult/" + str(type) + ".svg")
            plt.close()
            type += 1




    def _calculate_jcard_distance(self,center_list,l):
        result = []
        for idx,each_center_list in enumerate(center_list):
            num = 0
            for index,item in enumerate(l[0]):
                if item == each_center_list[0][index-1]:
                    num += 1
            result.append([idx,num])
        return result






if __name__ == '__main__':
    import time

    b = time.time()
    lib = proLib()
    # lib.cluster()
    # lib.k_mean(15)
    print(time.time() - b)
    df1 = lib.handle_file("D:\data\Stk_1F_2015\SH000001.csv")
    # lib.findSmilar(["SH000001.csv"],df1,1,5)
    lib.get_most_similar("D:\data\Stk_1F_2015\SH000001.csv",limit=5)
    lib.get_most_differ("D:\data\Stk_1F_2015\SH000001.csv", limit=5)
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
