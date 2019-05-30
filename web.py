import os

from flask import Flask, render_template, jsonify, request

from dataset import get_stock_data_detail, get_stock_data_day, find_most_similar, get_name_by_stock_id, \
    get_all_frequent_items, get_rules
from news_processing import get_news_by_date_str
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


@app.route('/similar')
def similar_assets():
    return render_template('similar.html')


@app.route('/clustering')
def clustering():
    return render_template('clustering.html')


@app.route('/freqitem')
def freq_itemset():
    return render_template('freqitem.html')


@app.route('/strategy/similarity')
def similarity_strategy():
    return render_template('strategy_similarity.html')


@app.route('/strategy/news')
def news_strategy():
    return render_template('strategy_news.html')


@app.route('/strategy/prediction')
def prediction_strategy():
    return


@app.route('/data/count')
def get_data_count():
    return jsonify({'count': len(os.listdir(DATA_DIR))})


@app.route('/data/stockList')
def _stock_list():
    stock_list = list()
    for f in os.listdir(DATA_DIR):
        stock_list.append(f.split('.')[0])
    return jsonify(stock_list)


@app.route('/data/stock/<stock_id>/name')
def get_stock_name(stock_id):
    return jsonify({'name': get_name_by_stock_id(stock_id)})


@app.route('/data/stock/detail/<stock_id>')
def stock_data_detail(stock_id):
    return jsonify(get_stock_data_detail(stock_id))


@app.route('/data/stock/day/<stock_id>')
def get_stock_data(stock_id):
    return jsonify(get_stock_data_day(stock_id))


@app.route('/data/news/<date_str>')
def get_news(date_str):
    return jsonify(get_news_by_date_str(date_str))


@app.route('/data/frequent_items')
def get_frequent_items():
    return jsonify(get_all_frequent_items())


@app.route('/data/rules',methods=['POST'])
def get_item_set_rules():
    data = request.json

    return jsonify(get_rules(data['reasons'], data['results']))


@app.route('/data/stock/similar/<stock_id>')
def get_most_similar(stock_id):
    limit = int(request.args.get('limit'))
    if not limit: limit = 5
    # return jsonify(
    #     [['SZ001979', 0.6666666666666666, 2, 3], ['SZ002602', 0.6, 9, 15], ['SZ399809', 0.5981308411214953, 64, 107],
    #      ['SZ399686', 0.5975609756097561, 49, 82], ['SH110031', 0.5909090909090909, 39, 66]])
    return jsonify(find_most_similar(stock_id, limit))


if __name__ == '__main__':
    app.run(host='10.20.63.0', port=1000)
