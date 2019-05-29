import os

from flask import Flask, render_template, jsonify

from dataset import get_stock_data_detail, get_stock_data_day
from settings import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', database_size=len(os.listdir(DATA_DIR)))


@app.route('/visualization')
def visualization():
    return render_template('visualization.html')


@app.route('/moving_average')
def moving_average():
    return render_template('moving_average.html')


@app.route('/data/count')
def get_data_count():
    return jsonify({'count': len(os.listdir(DATA_DIR))})


@app.route('/data/stockList')
def _stock_list():
    stock_list = list()
    for f in os.listdir(DATA_DIR):
        stock_list.append(f.split('.')[0])
    return jsonify(stock_list)


@app.route('/data/stock/detail/<stock_id>')
def stock_data_detail(stock_id):
    return jsonify(get_stock_data_detail(stock_id))


@app.route('/data/stock/day/<stock_id>')
def get_stock_data(stock_id):
    return jsonify(get_stock_data_day(stock_id))


if __name__ == '__main__':
    app.run(port=1000)
