import jieba
import fool
from py2neo import Graph
_graph = Graph(
        host='127.0.0.1', # neo4j 搭载服务器的ip地址
        http_port='7687', # neo4j 服务器监听的端口号
        user='neo4j', # 数据库user name，如果没有更改过，应该是neo4j
        password='AHyySZ0323' # 自己设定的密码
        )
province = [line.strip() for line in open("province.txt",encoding="utf-8").readlines()]
foreign_country = [line.strip() for line in open("foreign_countries.txt",encoding="utf-8").readlines()]
continent = [line.strip() for line in open("continent.txt",encoding="utf-8").readlines()]
confirmed = ['累计确诊']
curConfirm = ['当前确诊','现在的确诊','现在的','当前的','当前','现在','现有确诊','目前的','目前']
died = ['累计死亡','死亡','累计的死亡']
cured = ['累计治愈','累计治愈']

# 分词
def type_parse(question):
    jieba.load_userdict("my_dict.txt")
    words = jieba.cut(question.encode('utf-8'))
    for word in words:
        # print(word)
        if word in confirmed:
            return 'confirmed'
        if word in curConfirm:
            return 'curConfirm'
        if word in died:
            return 'died'
        if word in cured:
            return 'cured'

def location_parse(question):
    # 实体识别(地区)
    words, ners = fool.analysis(question)
    location_list = []
    for i in ners:
        for j in i:
            if j[2] == 'location' and j[3] in province:
                location_list.append(['domestic', j[3]])
            if j[2] == 'location' and j[3] in foreign_country:
                location_list.append(['foreign', j[3]])
            if j[2] == 'location' and j[3] in continent:
                location_list.append(['continent', j[3]])
            if j[2] == 'location' and j[3] == '中国':
                location_list.append(['china', j[3]])
    words = jieba.cut(question.encode('utf-8'))
    for word in words:
        if word in foreign_country:
            location_list.append(['foreign',word])
    return location_list

def match_type(search_type,location):
    sql = []
    if search_type == 'domestic_confirmed':  # 1. 查询国内某省市的累计确诊人数
        sql = ["MATCH (m:confirmed) where m.province='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'domestic_curConfirm':
        sql = ["MATCH (m:curConfirm) where m.province='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'domestic_died':
        sql = ["MATCH (m:died) where m.province='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'domestic_cured':
        sql = ["MATCH (m:cured) where m.province='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'foreign_confirmed':  # 2. 查询国外某国家的累计确诊人数
        sql = ["MATCH (m:confirmed) where m.country='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'foreign_curConfirm':
        sql = ["MATCH (m:curConfirm) where m.country='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'foreign_died':
        sql = ["MATCH (m:died) where m.country='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'foreign_cured':
        sql = ["MATCH (m:cured) where m.country='{0}' return m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        return data[0]['m.number']
    if search_type == 'continent_confirmed': # 查询大洲疫情情况
        sql = ["match(m:confirmed) where m.continent='{}' return m.country,m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        country_list = {}
        for i in range(len(data)):
            if data[i]['m.country'] not in country_list:
                country_list[data[i]['m.country']] = int(data[i]['m.number'])
        country_list = list(country_list.items())
        country_list.sort(key=lambda x: x[1], reverse=True)
        return country_list
    if search_type == 'continent_curConfirm':
        sql = ["match(m:curConfirm) where m.continent='{}' return m.country,m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        country_list = {}
        for i in range(len(data)):
            if data[i]['m.country'] not in country_list:
                country_list[data[i]['m.country']] = int(data[i]['m.number'])
        country_list = list(country_list.items())
        country_list.sort(key=lambda x: x[1], reverse=True)
        return country_list
    if search_type == 'continent_died':
        sql = ["match(m:died) where m.continent='{}' return m.country,m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        country_list = {}
        for i in range(len(data)):
            if data[i]['m.country'] not in country_list:
                country_list[data[i]['m.country']] = int(data[i]['m.number'])
        country_list = list(country_list.items())
        country_list.sort(key=lambda x: x[1], reverse=True)
        return country_list
    if search_type == 'continent_cured':
        sql = ["match(m:cured) where m.continent='{}' return m.country,m.number".format(location)]
        cur = _graph.run(sql[0])
        data = cur.data()
        country_list = {}
        for i in range(len(data)):
            if data[i]['m.country'] not in country_list:
                country_list[data[i]['m.country']] = int(data[i]['m.number'])
        country_list = list(country_list.items())
        country_list.sort(key=lambda x: x[1], reverse=True)
        return country_list
    if search_type == 'china_confirmed':# 查询中国疫情情况
        sql = ["match(m:province) where m.country='中国' return m.name;"]
        cur = _graph.run(sql[0])
        data = cur.data()
        province_list = []
        for i in range(len(data)):
            province_list.append(data[i]['m.name'])
        sum = 0
        for i in range(len(province_list)):
            sql = ["match(m:confirmed) where m.province='{}' return m.number".format(province_list[i])]
            cur = _graph.run(sql[0])
            data = cur.data()
            num = int(data[0]['m.number'])
            sum += num
        return sum
    if search_type == 'china_curConfirm':
        sql = ["match(m:province) where m.country='中国' return m.name;"]
        cur = _graph.run(sql[0])
        data = cur.data()
        province_list = []
        for i in range(len(data)):
            province_list.append(data[i]['m.name'])
        sum = 0
        for i in range(len(province_list)):
            sql = ["match(m:curConfirm) where m.province='{}' return m.number".format(province_list[i])]
            cur = _graph.run(sql[0])
            data = cur.data()
            num = int(data[0]['m.number'])
            sum += num
        return sum
    if search_type == 'china_died':
        sql = ["match(m:province) where m.country='中国' return m.name;"]
        cur = _graph.run(sql[0])
        data = cur.data()
        province_list = []
        for i in range(len(data)):
            province_list.append(data[i]['m.name'])
        sum = 0
        for i in range(len(province_list)):
            sql = ["match(m:died) where m.province='{}' return m.number".format(province_list[i])]
            cur = _graph.run(sql[0])
            data = cur.data()
            num = int(data[0]['m.number'])
            sum += num
        return sum
    if search_type == 'china_cured':
        sql = ["match(m:province) where m.country='中国' return m.name;"]
        cur = _graph.run(sql[0])
        data = cur.data()
        province_list = []
        for i in range(len(data)):
            province_list.append(data[i]['m.name'])
        sum = 0
        for i in range(len(province_list)):
            sql = ["match(m:cured) where m.province='{}' return m.number".format(province_list[i])]
            cur = _graph.run(sql[0])
            data = cur.data()
            num = int(data[0]['m.number'])
            sum += num
        return sum


if __name__=="__main__":
    question = input("Q:")
    location_list = location_parse(question)
    print(location_list)
    if location_list != []:
        type = type_parse(question)
        search_type = location_list[0][0] +'_' + type
        number = match_type(search_type,location_list[0][1])
        if location_list[0][0] != 'continent':
            if type == 'confirmed':
                print("A：{}的累计确诊人数为{}。".format(location_list[0][1],number))
            if type == 'curConfirm':
                print("A: {}的现有确诊人数为{}。".format(location_list[0][1],number))
            if type == 'died':
                print("A: {}的累计死亡人数为{}。".format(location_list[0][1],number))
            if type == 'cured':
                print("A: {}的累计治愈人数为{}。".format(location_list[0][1],number))
        else:
            name_all=[];num_all=[]
            for i in range(3):
                name,num = number[i]
                name_all.append([name,num])
            if type == 'confirmed':
                print("A：累计确诊，{}疫情较为严重的国家为{}。".format(location_list[0][1],name_all))
            if type == 'curConfirm':
                print("A：现有确诊，{}疫情较为严重的国家为{}。".format(location_list[0][1],name_all))
            if type == 'died':
                print("A：累计死亡，{}疫情较为严重的国家为{}。".format(location_list[0][1],name_all))
            if type == 'cured':
                print("A：累计治愈，{}疫情应对较好的国家为{}。".format(location_list[0][1],name_all))
    else:
        print('戴口罩，勤洗手，不扎堆，常通风。')


