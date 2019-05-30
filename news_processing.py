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
    data = '''
    [
    {
        "link": "http://business.sohu.com/20160130/n436420890.shtml",
        "title": "专访：中国有足够能力应对经济增长中所面临的问题——访经济学家曹远征",
        "matches": [
            "中国银行",
            "SH601988"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436424149.shtml",
        "title": "宽松环境造就反弹 A股下周预期需放低",
        "matches": [
            "中信证券",
            "SH600030"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436416639.shtml",
        "title": "首航直升机海南俱乐部成立提供救援等社会服务(图)",
        "matches": [
            "长白山",
            "SH603099"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436414862.shtml",
        "title": "股市周评：A股再回调　沪指跌破前期低点",
        "matches": [
            "创业板",
            "SZ159915"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436413768.shtml",
        "title": "大宗商品周评：金价涨势受阻　油价继续高歌猛进",
        "matches": [
            "大宗商品",
            "SZ161715"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436413766.shtml",
        "title": "黔源电力上半年将完成电厂7S管理验收",
        "matches": [
            "黔源电力",
            "SZ002039"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436412248.shtml",
        "title": "吉林向航天产业发力打造“卫星省”",
        "matches": [
            "航天信息",
            "SH600271"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436411055.shtml",
        "title": "炒白银投43万亏了42万 “高额回报”诱惑致血本无归",
        "matches": [
            "大宗商品",
            "SZ161715"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436414676.shtml",
        "title": "灿星已经不能再碰好声音?唐德和Talpa联手回应版权纠纷",
        "matches": [
            "唐德影视",
            "SZ300426"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436412705.shtml",
        "title": "北京“十二五”期间规模以上工业增加值年均增长6%",
        "matches": [
            "首钢股份",
            "SZ000959"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436411361.shtml",
        "title": "电子信息产业成湖北发展最快的支柱产业",
        "matches": [
            "信息技术",
            "SZ159939"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436407400.shtml",
        "title": "海尔：将“轻度整合”通用电气家电业务",
        "matches": [
            "青岛海尔",
            "SH600690"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436400340.shtml",
        "title": "走钢索的人(组图)",
        "matches": [
            "中国银行",
            "SH601988"
        ],
        "emotion": "neutral"
    },
    {
        "link": "http://business.sohu.com/20160130/n436409219.shtml",
        "title": "许小年再开炮：2750，我还嫌贵，还得继续跌！",
        "matches": [
            "中国建筑",
            "SH601668"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436400538.shtml",
        "title": "高盛：中国经济增速放缓的外溢影响被夸大",
        "matches": [
            "大宗商品",
            "SZ161715"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436397132.shtml",
        "title": "水井坊预告扭亏有望“摘帽”",
        "matches": [
            "水井坊",
            "SH600779"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436398067.shtml",
        "title": "“垄断行业”国企将行混合所有制改革增量试点",
        "matches": [
            "国企改",
            "SH501020"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436400749.shtml",
        "title": "多项政策门槛放宽 平行进口车利好频至",
        "matches": [
            "国机汽车",
            "SH600335"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436400624.shtml",
        "title": "1月中旬内蒙古动力煤坑口价环比止跌上涨 同比仍下降较大",
        "matches": [
            "鄂尔多斯",
            "SH600295"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436398781.shtml",
        "title": "美国强生公司全球裁员3000人 中国地区或受到波及",
        "matches": [
            "三诺生物",
            "SZ300298"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436398253.shtml",
        "title": "美联储再次加息或在6月 有助缓解中国资本外流压力",
        "matches": [
            "标普500",
            "SH513500"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436397414.shtml",
        "title": "2015年钢铁行业亏损645亿 产能过剩矛盾仍突出",
        "matches": [
            "武钢股份",
            "SH600005"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436397499.shtml",
        "title": "大唐集团湖南重点工程被指靠卖家产粉饰业绩",
        "matches": [
            "能源行业",
            "SH510610"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436398183.shtml",
        "title": "万亿元公开市场操作成降准 “替身” 央行打响汇率“保卫战”",
        "matches": [
            "国泰君安",
            "SH601211"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436395751.shtml",
        "title": "A股越来越坑 基金经理离职也越来越多了",
        "matches": [
            "南方天元",
            "SZ160133"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436393538.shtml",
        "title": "外资通过沪港通入场 A股正在筑底？",
        "matches": [
            "货币基金",
            "SH511620"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436397182.shtml",
        "title": "三桶油的低油价尴尬：海外油田进入高产期却下调产量",
        "matches": [
            "中国石化",
            "SH600028"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436394786.shtml",
        "title": "30省市政府报告重拳治霾 央企或“领跑” 碳排放交易",
        "matches": [
            "环境治理",
            "SH501030"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436395061.shtml",
        "title": "陕北千口“黑油井”隐现  “日赚一万”牵涉复杂利益链",
        "matches": [
            "中国石化",
            "SH600028"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436394275.shtml",
        "title": "钢铁供给侧改革：压缩1.5亿吨产能波及50万职工",
        "matches": [
            "国企改",
            "SH501020"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436390118.shtml",
        "title": "全球主要央行徘徊“变”与“不变”",
        "matches": [
            "大宗商品",
            "SZ161715"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436391288.shtml",
        "title": "任泽平：股市调整正在接近尾声 需降低投资预期",
        "matches": [
            "国企改",
            "SH501020"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436393425.shtml",
        "title": "八一钢铁被母公司输血难解亏损困境 停产做减法",
        "matches": [
            "宝钢股份",
            "SH600019"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436391168.shtml",
        "title": "工业企业向更高层面发展（市场观察）",
        "matches": [
            "材料行业",
            "SH510620"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436394567.shtml",
        "title": "国际油价暴跌中海油业绩承压 多部门减薪降福利",
        "matches": [
            "中国石化",
            "SH600028"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436389843.shtml",
        "title": "证券交易印花税同比增2.8倍 1亿股民人均贡献2553元",
        "matches": [
            "大宗商品",
            "SZ161715"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436391370.shtml",
        "title": "一周财经：去年23省份GDP增速超7% 国企利润降6.7%(组图)",
        "matches": [
            "国企改",
            "SH501020"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436390462.shtml",
        "title": "国际油价断崖式下跌 中石油净利润预减70%",
        "matches": [
            "中国石油",
            "SH601857"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388149.shtml",
        "title": "消费税征税范围将扩大 高耗能高档消费品等或被纳入",
        "matches": [
            "能源行业",
            "SH510610"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436397213.shtml",
        "title": "聚焦农民增收，今年中央“一号文件”有何高招？(图)",
        "matches": [
            "建设银行",
            "SH601939"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436392199.shtml",
        "title": "俄回应普京纪录片：毫无根据！(组图)",
        "matches": [
            "新华网",
            "SH603888"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388383.shtml",
        "title": "证监会发布开年A股市场主要数据",
        "matches": [
            "中文在线",
            "SZ300364"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388351.shtml",
        "title": "证监会：两融各项指标处于安全状况",
        "matches": [
            "西南证券",
            "SH600369"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388350.shtml",
        "title": "格力正式起诉美的举报者 技术造假之争再升级",
        "matches": [
            "美的集团",
            "SZ000333"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436387673.shtml",
        "title": "安倍重臣因受贿丑闻辞职 收受建筑公司高管贿赂",
        "matches": [
            "太平洋",
            "SH601099"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388385.shtml",
        "title": "一月A股正式收官 沪指创历史最差开年行情",
        "matches": [
            "创业板",
            "SZ159915"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388349.shtml",
        "title": "证监会：200余亿元融资余额低于平仓线",
        "matches": [
            "港股通",
            "SH501309"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436387608.shtml",
        "title": "10中管干部被“断崖式”降级 5人涉地产拆迁",
        "matches": [
            "东风汽车",
            "SH600006"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388352.shtml",
        "title": "高校独董被查再度拷问独董制度",
        "matches": [
            "医药行业",
            "SH510660"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388027.shtml",
        "title": "格力1代手机出货量五六万台 董小姐跟手机较劲",
        "matches": [
            "格力电器",
            "SZ000651"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388947.shtml",
        "title": "中海油尼克森项目噩梦不断 多个部门减薪降福利",
        "matches": [
            "中国石化",
            "SH600028"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388576.shtml",
        "title": "中海集运2015年预亏28亿元 大批船员收入下降或半失业",
        "matches": [
            "国企改",
            "SH501020"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436388473.shtml",
        "title": "茅台旺季遇冷罚销售 利润触底经销商心寒求退场",
        "matches": [
            "贵州茅台",
            "SH600519"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381933.shtml",
        "title": "北京下调工伤保险费率",
        "matches": [
            "环境治理",
            "SH501030"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381585.shtml",
        "title": "与其无休止地向自然索取，还不如好好向它学习(图)",
        "matches": [
            "太阳能",
            "SZ000591"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381698.shtml",
        "title": "中国式照相馆审美：从写实到“PS”(组图)",
        "matches": [
            "新文化",
            "SZ300336"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381311.shtml",
        "title": "6000万美元，唐德拿下“好声音”版权(图)",
        "matches": [
            "唐德影视",
            "SZ300426"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381696.shtml",
        "title": "对话徐宁：文明夹缝中的女性世界(2)(组图)",
        "matches": [
            "新文化",
            "SZ300336"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436381211.shtml",
        "title": "股票质押平仓线下融资余额200亿(图)",
        "matches": [
            "锡业股份",
            "SZ000960"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436375965.shtml",
        "title": "曾俊华：流入香港的1300亿美元或将随美元加息逐渐流走",
        "matches": [
            "货币基金",
            "SH511620"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436416464.shtml",
        "title": "天津同仁堂、狗不理挂牌上市　新三板成老字号融资新平台",
        "matches": [
            "同仁堂",
            "SH600085"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436416197.shtml",
        "title": "收购服装公司失败 美邦宣布2月1日复牌",
        "matches": [
            "美邦服饰",
            "SZ002269"
        ],
        "emotion": "negative"
    },
    {
        "link": "http://business.sohu.com/20160130/n436416046.shtml",
        "title": "福建平潭：逆势而攀登　向海而致远",
        "matches": [
            "跨境通",
            "SZ002640"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436413781.shtml",
        "title": "海尔：与通用电气家电的整合将是“轻度”的",
        "matches": [
            "青岛海尔",
            "SH600690"
        ],
        "emotion": "positive"
    },
    {
        "link": "http://business.sohu.com/20160130/n436389794.shtml",
        "title": "央行两周“放水”逾2万亿元 春节资金缺口将基本填补",
        "matches": [
            "兴业银行",
            "SH601166"
        ],
        "emotion": "positive"
    }
]
    '''
    d = json.loads(data)
    for i in range(len(d)):
        name, sid = d[i]['matches']

        del d[i]['matches']
        d[i]['stock'] = sid + ' ' + name
        d[i]['title'] = '<a href="{link}">{title}</a>'.format(link=d[i]['link'], title=d[i]['title'])
        del d[i]['link']
    print(json.dumps(d, ensure_ascii=False))
