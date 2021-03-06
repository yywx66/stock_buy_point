import baostock as bs
import pandas as pd
import datetime 
from chinese_calendar import is_workday
import numpy as np

# 机构重仓
jigou_2020Q1 = ['长电科技', '卫宁健康', '东山精密', '上海机场', '中炬高新', '沃森生物', '潍柴动力', '华测检测', '健帆生物', '中国建筑',
                '汇川技术', '冀东水泥', '天坛生物', '康泰生物', '美年健康', '药明康德', '三七互娱', '智飞生物', '益丰药房', '歌尔股份',
                '北方华创', '海螺水泥', '爱尔眼科', '华域汽车', '先导智能', '光环新网', '上汽集团', '南极电商', '华天科技', '深南电路',
                '东方雨虹', '三安光电', '永辉超市', '太阳纸业', '生物股份', '圣邦股份', '中国中免', '泰格医药', '浪潮信息', '格力电器',
                '宁德时代', '海大集团', '普洛药业', '中国中车', '中国铁建', '洋河股份', '中国神华', '用友网络', '兆易创新', '立讯精密',
                '海康威视', '山西汾酒', '晨光文具', '海天味业', '顺网科技', '生益科技', '晶方科技', '东华软件', '海尔智家', '迈瑞医疗',
                '科大讯飞', '山东药玻', '牧原股份', '洽洽食品', '通策医疗', '美亚柏科', '安井食品', '韦尔股份', '中航光电', '分众传媒',
                '芒果超媒', '长春高新', '美的集团', '温氏股份', '中国石化', '复星医药', '绝味食品', '山东黄金', '三一重工', '闻泰科技',
                '北新建材', '万华化学', '顺鑫农业', '华兰生物', '我武生物', '光威复材', '通威股份', '扬农化工', '华鲁恒升', '双汇发展',
                '赣锋锂业', '中公教育', '国瓷材料', '烽火通信', '沪电股份', '中科曙光', '紫金矿业', '京沪高铁', '亿联网络', '中信特钢',
                '宇通客车', '长江电力', '金风科技', '宋城演艺', '东方财富', '隆基股份', '乐普医疗', '古井贡酒', '安图生物', '壹网壹创',
                '恒立液压', '伊利股份', '金山办公', '中环股份', '视源股份', '国电南瑞', '顺丰控股', '启明星辰', '金域医学', '完美世界',
                '贵州茅台', '汇顶科技', '信维通信', '高德红外', '中国软件', '中顺洁柔', '亿纬锂能', '泸州老窖', '恒生电子', '康弘药业',
                '比亚迪', '健友股份', '三花智控', '中兴通讯', '恒瑞医药', '深信服', '吉比特', '大参林', '新希望', '家家悦',
                '凯莱英', '广联达', '五粮液', '欣旺达', '老百姓',   '苏泊尔', '京东方A', '卓胜微']

jigou_2020Q2 = ['贵州茅台', '立讯精密', '长春高新', '隆基股份', '恒瑞医药', '中国中免', '宁德时代', '迈瑞医疗', '美的集团', '泸州老窖',
                '药明康德', '东方财富', '伊利股份', '恒生电子', '三一重工', '格力电器', '芒果超媒', '亿纬锂能', '顺丰控股', '爱尔眼科',
                '万华化学', '海康威视', '康泰生物', '山西汾酒', '通威股份', '兆易创新', '海大集团', '三安光电', '三花智控', '三七互娱',
                '歌尔股份', '东方雨虹', '通策医疗', '智飞生物', '中兴通讯', '汇川技术', '双汇发展', '紫金矿业', '海尔智家', '金山办公',
                '古井贡酒', '分众传媒', '美年健康', '华鲁恒升', '用友网络', '南极电商', '泰格医药', '圣邦股份', '华兰生物', '华测检测',
                '健帆生物', '蓝思科技', '华海药业', '绝味食品', '信维通信', '洋河股份', '顺鑫农业', '海天味业', '沃森生物', '赣锋锂业',
                '牧原股份', '北方华创', '中炬高新', '长电科技', '上海机场', '海螺水泥', '闻泰科技', '山东药玻', '宋城演艺', '星宇股份',
                '完美世界', '金域医学', '安井食品', '中科曙光', '永辉超市', '紫光国微', '国瓷材料', '华域汽车', '卫宁健康', '安琪酵母',
                '紫光股份', '中科创达', '浪潮信息', '太阳纸业', '中国建筑', '韦尔股份', '我武生物', '中航光电', '乐普医疗', '晨光文具',
                '宝信软件', '中公教育', '京沪高铁', '人福医药', '涪陵榨菜', '安图生物', '东山精密', '欧普康视', '北新建材', '亿联网络',
                '光威复材', '康龙化成', '中国巨石', '先导智能', '普洛药业', '复星医药', '中航沈飞', '益丰药房', '中国软件', '视源股份',
                '贝达药业', '浙江鼎力', '建设机械', '云南白药', '重庆啤酒', '宏发股份', '光线传媒', '洽洽食品', '青岛啤酒', '高德红外',
                '捷佳伟创', '生益科技', '长江电力', '恩捷股份', '风华高科', '航发动力', '英科医疗', '天赐材料', '温氏股份', '中环股份', 
                '潍柴动力', '京东方A', '吉比特', 'TCL科技', '深信服', '比亚迪', '片仔癀', '今世缘', '新宙邦', '卓胜微', 
                '欣旺达', '五粮液', '广联达', '凯莱英', '璞泰来', '司太立', '同花顺', '中国神华', '福斯特', '掌趣科技']

jigou_2020Q3 = ['贵州茅台', '五粮液', '宁德时代', '美的集团', '海天味业', '恒瑞医药', '迈瑞医疗', '长江电力', '海康威视', '比亚迪',
             '中国中免', '立讯精密', '顺丰控股', '格力电器', '隆基股份', '京沪高铁', '药明康德', '牧原股份', '海螺水泥', '爱尔眼科',
             '智飞生物', '洋河股份', '泸州老窖', '万华化学', '中公教育', '伊利股份', '中芯国际', '三一重工', '中国建筑', '山西汾酒',
             '长城汽车', '双汇发展', '韦尔股份', '紫金矿业', '京东方A', '海尔智家', '长春高新', '金山办公', '歌尔股份', '蓝思科技',
             '用友网络', '分众传媒', '中兴通讯', '芒果超媒', '通威股份', '荣盛石化', '上海机场', '闻泰科技', '中国广核', '康泰生物',
             '鹏鼎控股', '汇川技术', '泰格医药', '三安光电', '海大集团', '恒立液压', '华域汽车', '亿纬锂能', '航发动力', '恒生电子',
             '华兰生物', '兆易创新', '领益智造', '古井贡酒', '福耀玻璃', '康龙化成', '三花智控', '恩捷股份', '东方雨虹', '中微公司',
             '北方华创', '广联达', 'TCL科技', '卓胜微', '深信服', '沃森生物', '赣锋锂业', '安图生物', '晨光文具', '永辉超市',
             '欧派家居', '中航沈飞', '通策医疗', '中环股份', '视源股份', '美年健康', '凯莱英', '紫光国微', '今世缘', '健帆生物',
             '正泰电器', '三七互娱', '宝信软件', '中航光电', '长电科技', '福斯特', '北新建材', '阳光电源', '亿联网络', '完美世界',
             '益丰药房', '三环集团', '高德红外', '先导智能', '重庆啤酒', '中炬高新', '绝味食品', '华海药业', '中国巨石', '璞泰来',
             '金域医学', '中科曙光', '华鲁恒升', '信维通信', '南极电商', '顾家家居', '星宇股份', '华测检测', '人福医药', '浙江鼎力', 
             '欣旺达', '安琪酵母', '宋城演艺', '东山精密', '圣邦股份', '安井食品', '欧普康视', '中航机电', '顺鑫农业', '国瓷材料',
             '英科医疗', '中科创达', '太阳纸业', '新宝股份', '宇通客车', '百润股份', '光威复材', '天赐材料', '吉比特', '水井坊', 
             '航天发展', '捷佳伟创', '我武生物', '新宙邦', '扬农化工', '九洲药业', '生物股份', '博腾股份', '法拉电子', '航天电器']

jigou = jigou_2020Q1 + jigou_2020Q2 + jigou_2020Q3

# 北上资金前50
North50_2020Q1 = ['牧原股份', '顺丰控股', '韦尔股份', '潍柴动力', '三七互娱', '隆基股份', '宁德时代', '东方雨虹', '华兰生物', '国电南瑞',
                  '药明康德', '生物股份', '三一重工', '迈瑞医疗', '立讯精密', '汇川技术', '保利地产', '泰格医药', '恒生电子', '中信证券',
                  '恒立液压', '海天味业', '海康威视', '美的集团', '伊利股份', '贵州茅台', '长江电力', '招商银行', '华测检测', '万华化学',
                  '工商银行', '分众传媒', '格力电器', '中国平安', '方正证券', '恒瑞医药', '云南白药', '上海机场', '海螺水泥', '上汽集团',
                  '平安银行', '海尔智家', '洋河股份', '中国中免', '兴业银行', '爱尔眼科', '京东方A', '万科A', '五粮液', '广联达', ]

North50_2020Q3 = ['比亚迪', '恒立液压', '潍柴动力', '宁德时代', '中国建筑', '牧原股份', '分众传媒', '国电南瑞', '顺丰控股', '万科A',
                 '京东方A', '立讯精密', '平安银行', '格力电器', '迈瑞医疗', '三七互娱', '华测检测', '中信证券', '万华化学', '恒生电子',
                 '海螺水泥', '上海机场', '三一重工', '伊利股份', '中国平安', '上汽集团', '福耀玻璃', '恒瑞医药', '海康威视', '方正证券',
                 '东方雨虹', '海天味业', '益丰药房', '招商银行', '爱尔眼科', '云南白药', '广联达', '兴业银行', '长江电力', '贵州茅台',
                 '保利地产', '美的集团', '药明康德', '泰格医药', '隆基股份', '洋河股份', '汇川技术', '中国中免', '海尔智家', '五粮液']

North50 = North50_2020Q1 + North50_2020Q3

ZiXuan = ['美亚光电', '大华股份', '中信建投', '上海新阳', '苏州固锝', '老板电器', '上海贝岭', '伟明环保', '中国太保', '珠江啤酒', 
          '上峰水泥', '宏发股份', '德赛西威', '涪陵榨菜', '光线传媒', '中航高科', '捷捷微电', '通富微电', '三只松鼠', '良品铺子',
          '中国长城', '南大光电', '得润电子', '安洁科技', '晶盛机电', '燕京啤酒', '江西铜业', '均胜电子', '中材科技', '中航重机',
          '德邦股份', '长安汽车', '春秋航空', '桃李面包', '中直股份', '航发控制', '光明乳业', '中国人寿', '联美控股', '重庆啤酒',
          '福成股份', '超图软件', '士兰微', '中科软', '新洋丰', '福莱特', '科沃斯', '白云山', '利亚德', '张裕A', '金达威']

Champion = ['贝瑞基因', '迪安诊断', '顺网科技', '密尔克卫', '富邦股份', '金城医药', '广州酒家', '博实股份', '巨星科技', '安车检测',
            '杭叉集团', '智莱科技', '杭锅股份', '雪榕生物', '华宏科技', '苏试试验', '飞荣达', '爱柯迪', '溢多利', '康力电梯','宁波银行']

# 北上前50 + 机构重仓集合
better_stocks = list(set(jigou + North50 + Champion + ZiXuan)) 
print(len(set(better_stocks))) # 261

def get_all_data():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock(day="2020-07-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        all_stocks.append(rs_all.get_row_data())

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./stocks-pool/all_stocks.csv", encoding="gbk", index=False)
    return stocks_result

def get_better_stocks():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock("2020-07-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        code_info = rs_all.get_row_data()
        if code_info[2] in better_stocks:
            all_stocks.append(code_info)

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./stocks-pool/better_stocks.csv", encoding="gbk", index=False)
    return stocks_result

# 沪深300 + 中证500
def get_hs300_zz500_data():
    # 获取沪深300和中证500成分股
    rs_hs300 = bs.query_hs300_stocks("2020-07-30")
    rs_zz500 = bs.query_zz500_stocks("2020-07-30")
    print('query_hs300 error_code:' + rs_hs300.error_code)
    print('query_hs300  error_msg:' + rs_hs300.error_msg)
    print('query_zz500 error_code:' + rs_zz500.error_code)
    print('query_zz500  error_msg:' + rs_zz500.error_msg)

    # 打印结果集
    hs300_stocks = []
    zz500_stocks = []
    while (rs_hs300.error_code == '0') & rs_hs300.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs_hs300.get_row_data())
    while (rs_zz500.error_code == '0') & rs_zz500.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs_zz500.get_row_data())

    stocks_result = pd.DataFrame(hs300_stocks+zz500_stocks, columns=rs_hs300.fields)

    # stocks_result.to_csv("./stocks-pool/hs300_zz500_stocks.csv", encoding="gbk", index=False)
    return stocks_result

if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # data = get_hs300_zz500_data()
    # print(data)

    data = pd.read_csv("./stocks-pool/all_stocks.csv", encoding='gbk')
    # print(data['code_name'].values.tolist())
    for i in better_stocks:
        if i not in data['code_name'].values.tolist():
            print(i)

    #### 登出系统 ####
    bs.logout()

