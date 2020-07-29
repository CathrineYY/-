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
curConfirm = ['当前确诊','现在的确诊','现在的','当前的','当前','现在','现有确诊','目前的','目前','目前的确诊']
died = ['累计死亡','死亡','累计的死亡']
cured = ['累计治愈','累计治愈','治愈情况']
nameMap = {
        'Singapore Rep.':'新加坡',
        'Dominican Rep.':'多米尼加',
        'Palestine':'巴勒斯坦',
        'Bahamas':'巴哈马',
        'Timor-Leste':'东帝汶',
        'Afghanistan':'阿富汗',
        'Guinea-Bissau':'几内亚比绍',
        "Côte d'Ivoire":'科特迪瓦',
        'Siachen Glacier':'锡亚琴冰川',
        "Br. Indian Ocean Ter.":'英属印度洋领土',
        'Angola':'安哥拉',
        'Albania':'阿尔巴尼亚',
        'United Arab Emirates':'阿联酋',
        'Argentina':'阿根廷',
        'Armenia':'亚美尼亚',
        'French Southern and Antarctic Lands':'法属南半球和南极领地',
        'Australia':'澳大利亚',
        'Austria':'奥地利',
        'Azerbaijan':'阿塞拜疆',
        'Burundi':'布隆迪',
        'Belgium':'比利时',
        'Benin':'贝宁',
        'Burkina Faso':'布基纳法索',
        'Bangladesh':'孟加拉国',
        'Bulgaria':'保加利亚',
        'The Bahamas':'巴哈马',
        'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
        'Belarus':'白俄罗斯',
        'Belize':'伯利兹',
        'Bermuda':'百慕大',
        'Bolivia':'玻利维亚',
        'Brazil':'巴西',
        'Brunei':'文莱',
        'Bhutan':'不丹',
        'Botswana':'博茨瓦纳',
        'Central African Rep.':'中非',
        'Canada':'加拿大',
        'Switzerland':'瑞士',
        'Chile':'智利',
        'China':'中国',
        'Ivory Coast':'象牙海岸',
        'Cameroon':'喀麦隆',
        'Dem. Rep. Congo':'刚果民主共和国',
        'Congo':'刚果',
        'Colombia':'哥伦比亚',
        'Costa Rica':'哥斯达黎加',
        'Cuba':'古巴',
        'N. Cyprus':'北塞浦路斯',
        'Cyprus':'塞浦路斯',
        'Czech Rep.':'捷克',
        'Germany':'德国',
        'Djibouti':'吉布提',
        'Denmark':'丹麦',
        'Algeria':'阿尔及利亚',
        'Ecuador':'厄瓜多尔',
        'Egypt':'埃及',
        'Eritrea':'厄立特里亚',
        'Spain':'西班牙',
        'Estonia':'爱沙尼亚',
        'Ethiopia':'埃塞俄比亚',
        'Finland':'芬兰',
        'Fiji':'斐',
        'Falkland Islands':'福克兰群岛',
        'France':'法国',
        'Gabon':'加蓬',
        'United Kingdom':'英国',
        'Georgia':'格鲁吉亚',
        'Ghana':'加纳',
        'Guinea':'几内亚',
        'Gambia':'冈比亚',
        'Guinea Bissau':'几内亚比绍',
        'Eq. Guinea':'赤道几内亚',
        'Greece':'希腊',
        'Greenland':'格陵兰',
        'Guatemala':'危地马拉',
        'French Guiana':'法属圭亚那',
        'Guyana':'圭亚那',
        'Honduras':'洪都拉斯',
        'Croatia':'克罗地亚',
        'Haiti':'海地',
        'Hungary':'匈牙利',
        'Indonesia':'印度尼西亚',
        'India':'印度',
        'Ireland':'爱尔兰',
        'Iran':'伊朗',
        'Iraq':'伊拉克',
        'Iceland':'冰岛',
        'Israel':'以色列',
        'Italy':'意大利',
        'Jamaica':'牙买加',
        'Jordan':'约旦',
        'Japan':'日本',
        'Japan':'日本本土',
        'Kazakhstan':'哈萨克斯坦',
        'Kenya':'肯尼亚',
        'Kyrgyzstan':'吉尔吉斯斯坦',
        'Cambodia':'柬埔寨',
        'Korea':'韩国',
        'Kosovo':'科索沃',
        'Kuwait':'科威特',
        'Lao PDR':'老挝',
        'Lebanon':'黎巴嫩',
        'Liberia':'利比里亚',
        'Libya':'利比亚',
        'Sri Lanka':'斯里兰卡',
        'Lesotho':'莱索托',
        'Lithuania':'立陶宛',
        'Luxembourg':'卢森堡',
        'Latvia':'拉脱维亚',
        'Morocco':'摩洛哥',
        'Moldova':'摩尔多瓦',
        'Madagascar':'马达加斯加',
        'Mexico':'墨西哥',
        'Macedonia':'马其顿',
        'Mali':'马里',
        'Myanmar':'缅甸',
        'Montenegro':'黑山',
        'Mongolia':'蒙古',
        'Mozambique':'莫桑比克',
        'Mauritania':'毛里塔尼亚',
        'Malawi':'马拉维',
        'Malaysia':'马来西亚',
        'Namibia':'纳米比亚',
        'New Caledonia':'新喀里多尼亚',
        'Niger':'尼日尔',
        'Nigeria':'尼日利亚',
        'Nicaragua':'尼加拉瓜',
        'Netherlands':'荷兰',
        'Norway':'挪威',
        'Nepal':'尼泊尔',
        'New Zealand':'新西兰',
        'Oman':'阿曼',
        'Pakistan':'巴基斯坦',
        'Panama':'巴拿马',
        'Peru':'秘鲁',
        'Philippines':'菲律宾',
        'Papua New Guinea':'巴布亚新几内亚',
        'Poland':'波兰',
        'Puerto Rico':'波多黎各',
        'Dem. Rep. Korea':'朝鲜',
        'Portugal':'葡萄牙',
        'Paraguay':'巴拉圭',
        'Qatar':'卡塔尔',
        'Romania':'罗马尼亚',
        'Russia':'俄罗斯',
        'Rwanda':'卢旺达',
        'W. Sahara':'西撒哈拉',
        'Saudi Arabia':'沙特阿拉伯',
        'Sudan':'苏丹',
        'S. Sudan':'南苏丹',
        'Senegal':'塞内加尔',
        'Solomon Is.':'所罗门群岛',
        'Sierra Leone':'塞拉利昂',
        'El Salvador':'萨尔瓦多',
        'Somaliland':'索马里兰',
        'Somalia':'索马里',
        'Serbia':'塞尔维亚',
        'Suriname':'苏里南',
        'Slovakia':'斯洛伐克',
        'Slovenia':'斯洛文尼亚',
        'Sweden':'瑞典',
        'Swaziland':'斯威士兰',
        'Syria':'叙利亚',
        'Chad':'乍得',
        'Togo':'多哥',
        'Thailand':'泰国',
        'Tajikistan':'塔吉克斯坦',
        'Turkmenistan':'土库曼斯坦',
        'East Timor':'东帝汶',
        'Trinidad and Tobago':'特里尼达和多巴哥',
        'Tunisia':'突尼斯',
        'Turkey':'土耳其',
        'Tanzania':'坦桑尼亚',
        'Uganda':'乌干达',
        'Ukraine':'乌克兰',
        'Uruguay':'乌拉圭',
        'United States':'美国',
        'Uzbekistan':'乌兹别克斯坦',
        'Venezuela':'委内瑞拉',
        'Vietnam':'越南',
        'Vanuatu':'瓦努阿图',
        'West Bank':'西岸',
        'Yemen':'也门',
        'South Africa':'南非',
        'Zambia':'赞比亚',
        'Zimbabwe':'津巴布韦'
}
nameMap = list(nameMap.items())

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
            location_list.append(['foreign', word])
        elif word == '我国':
            location_list.append(['china', word])
        else:
            if word == 'America' or word == 'United_States':
                word = 'United States'
            if word == 'Britain':
                word = 'United Kingdom'
            for i in range(len(nameMap)):
                key, value = nameMap[i]
                if key == word:
                    w = value
                    if w in foreign_country:
                        location_list.append(['foreign', w])
                    if w == '中国':
                        location_list.append(['china', w])
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


# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request

# 实例化，可视为固定格式
app = Flask(__name__)

# route()方法用于设定路由；类似spring路由配置
#等价于在方法后写：app.add_url_rule('/', 'helloworld', hello_world)
@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

# 配置路由，当请求get.html时交由get_html()处理
@app.route('/get.html')
def get_html():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('KBAQ.html')

# 配置路由，当请求post.html时交由post_html()处理
@app.route('/')
def post_html():
    # 使用render_template()方法重定向到templates文件夹下查找post.html文件
    return render_template('KBAQ.html')

# 配置路由，当请求deal_request时交由deal_request()处理
# 默认处理get请求，我们通过methods参数指明也处理post请求
# 当然还可以直接指定methods = ['POST']只处理post请求, 这样下面就不需要if了
@app.route('/deal_request', methods = ['GET', 'POST'])
def deal_request():
    if request.method == "GET":
        # get通过request.args.get("param_name","")形式获取参数值
        get_q = request.args.get("q","")
        return render_template("result.html", result1=get_q)
    elif request.method == "POST":
        # post通过request.form["param_name"]形式获取参数值
        post_q = request.form["q"]
        result2 = 'A'
        if post_q!= 'A' :
            question = post_q
            location_list = location_parse(question)
            if location_list != []:
                type = type_parse(question)
                search_type = location_list[0][0] + '_' + type
                number = match_type(search_type, location_list[0][1])
                if location_list[0][0] != 'continent':
                    if type == 'confirmed':
                        result2="[A]：{}的累计确诊人数为{}。".format(location_list[0][1], number)
                    if type == 'curConfirm':
                        result2="[A]: {}的现有确诊人数为{}。".format(location_list[0][1], number)
                    if type == 'died':
                        result2="[A]: {}的累计死亡人数为{}。".format(location_list[0][1], number)
                    if type == 'cured':
                        result2="[A]: {}的累计治愈人数为{}。".format(location_list[0][1], number)
                else:
                    name_all = []
                    sum_all = 0
                    for i in range(3):
                        name, num = number[i]
                        name_all.append([name, num])
                    for i in range(len(number)):
                        name,num = number[i]
                        sum_all+=num
                    if type == 'confirmed':
                        result2="[A]：累计确诊{}例，{}疫情较为严重的国家为{}。".format(sum_all,location_list[0][1], name_all)
                    if type == 'curConfirm':
                        result2="[A]：现有确诊{}例，{}疫情较为严重的国家为{}。".format(sum_all,location_list[0][1], name_all)
                    if type == 'died':
                        result2="[A]：累计死亡{}例，{}疫情较为严重的国家为{}。".format(sum_all,location_list[0][1], name_all)
                    if type == 'cured':
                        result2 ="[A]：累计治愈{}例，{}疫情应对较好的国家为{}。".format(sum_all,location_list[0][1], name_all)
            else:
                result2 ="[A]:戴口罩，勤洗手，不扎堆，常通风。"
        return render_template("result.html", result=post_q,result2=result2)


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)