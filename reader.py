import datetime
import os
import sys

import pandas

CHUNK_SIZE = 10 ** 8
HEADERS_DISPLAY_NAME = ['日期', '时间', '开盘价', '最高价', '最低价', '收盘价(元)', '成交金额(百万)', '成交量']
HEADERS_VAR_NAME = ['date', 'time', 'open_price', 'max_price', 'min_price', 'close_price', 'turnover', 'volume']


def readfile(filename):
    if not os.path.isfile(filename):
        sys.stderr.write('Error: file not found.\n')
        sys.exit(1)
    for chunk in pandas.read_csv(filename, chunksize=CHUNK_SIZE, names=HEADERS_DISPLAY_NAME):
        for i, row in chunk.iterrows():
            yield (i, row)


def readfile_day(filename):
    curr_date = 0
    data = list()
    for i, row in readfile(filename):

        _date, _time, open_price, max_price, min_price, close_price, turnover, volume = row
        _date = int(''.join(_date.split('/')))
        if i == 0:
            curr_date = _date

        if curr_date < _date:  # entering next day
            yield datetime.datetime.strptime(str(curr_date), '%Y%m%d'), data
            curr_date = _date
            data = [row]
        else:
            data.append(row)
    yield datetime.datetime.strptime(str(curr_date), '%Y%m%d'), data


def readfile_day_aggr(filename):
    if not os.path.isfile(filename):
        sys.stderr.write('Error: file not found.\n')
        sys.exit(1)
    df = pandas.read_csv(filename, names=HEADERS_DISPLAY_NAME)
    grouped = df.groupby('日期')
    ret = list()
    # date, time, open_price, highest, lowest, close, amount, volume
    for name, group in grouped:
        day_open = float(group.head(1)['开盘价'])
        day_close = float(group.tail(1)['收盘价(元)'])
        day_max = float(group['最高价'].max())
        day_min = float(group['最低价'].min())
        day_amount = float(group['成交金额(百万)'].sum())
        day_volume = float(group['成交量'].sum())
        yield [name, '', day_open, day_max, day_min, day_close, day_amount, day_volume]
