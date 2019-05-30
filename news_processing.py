news_dir = r'D:\news_data\sohu-20130820-20161031'
out_dir = r'D:\news_data\out'
match_dir = r'D:\news_data\match'
import json
import os


def pre_processing():
    for fn in os.listdir(news_dir):
        with open(os.path.join(news_dir, fn), encoding='utf8') as f:
            print('Processing', fn)
            with open(os.path.join(out_dir, fn), 'w', encoding='utf8') as f2:
                for line in f:
                    if 'business.sohu.com' in line:
                        f2.write('|'.join(line.split('`1`2')))


def match_keywords():
    with open('code.json', encoding='utf8') as f:
        code = json.load(f)
    for fn in os.listdir(out_dir):
        with open(os.path.join(out_dir, fn), encoding='utf8') as f:
            print('Processing', fn)
            with open(os.path.join(match_dir, fn), 'w', encoding='utf8') as f2:
                file_matches = list()
                for line in f:
                    single_news_matches = list()
                    for c in code:
                        if c[0] in line or c[1] in line:
                            single_news_matches.append(c)
                    if single_news_matches:
                        file_matches.append({
                            'content': line,
                            'matches': single_news_matches
                        })
                json.dump(file_matches, f2, ensure_ascii=False, indent=2)


def get_news_by_date_str(date_str):
    file_path = os.path.join(match_dir, date_str)
    if not os.path.isfile(file_path):
        return list()
    ret = list()
    with open(file_path, encoding='utf8') as f:
        news_data = json.load(f)
        for d in news_data:
            link, title, text = d['content'].split('|', 2)
            ret.append({
                'link': link,
                'title': title,
                'matches': d['matches']
            })
    return ret


if __name__ == '__main__':
    print(get_news_by_date_str('20160101'))
