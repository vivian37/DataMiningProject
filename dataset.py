import os

from proLib import proLib
from reader import readfile_day_aggr
from settings import *

plib = proLib()


def get_stock_data_detail(stock_id):
    data = list()
    with open(os.path.join(DATA_DIR, '{}.csv'.format(stock_id))) as f:
        for l in f:
            date, time, open_price, highest, lowest, close, amount, volume = l.split(',')
            if open_price > close:
                sign = -1
            if open_price < close:
                sign = 1
            else:
                sign = 1

            data.append(
                [date + ' ' + time, float(open_price), float(highest), float(lowest), float(close), float(volume),
                 sign])
    return data


def get_stock_data_day(stock_id):
    """
    date, open, close ,min, max
    :param stock_id:
    :return:
    """
    data = list(readfile_day_aggr(os.path.join(DATA_DIR, '{}.csv'.format(stock_id))))
    data = [[d[0], float(d[2]), float(d[5]), float(d[4]), float(d[3])] for d in data]
    return data


def find_most_similar(stock_id, limit):
    return plib.get_most_similar(os.path.join(DATA_DIR, stock_id + '.csv'), limit)


def get_stock_data_day_pct(stock_id):
    """
    date, open, close +=pct
    :param stock_id:
    :return:
    """
    data = list(readfile_day_aggr(os.path.join(DATA_DIR, '{}.csv'.format(stock_id))))
    data = [[d[0], float(d[2]), float(d[5]), (float(d[2]) - float(d[5])) / float(d[5])] for d in data]
    return data


