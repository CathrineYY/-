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
confirmed = ['累计确诊']
curConfirm = ['当前确诊','现在的确诊','现在的','当前的','当前','现在']
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
        # if post_q!= NULL :
        #     question = post_q
        #     location_list = location_parse(question)
        #     type = type_parse(question)
        #     search_type = location_list[0][0] + '_' + type
        #     number = match_type(search_type, location_list[0][1])
        #     if type == 'confirmed':
        #         result2 = "A：{}的累计确诊人数为{}。".format(location_list[0][1], number)
        #     if type == 'curConfirm':
        #         result2 = "A: {}的现有确诊人数为{}。".format(location_list[0][1], number)
        #     if type == 'died':
        #         result2 = "A: {}的累计死亡人数为{}。".format(location_list[0][1], number)
        #     if type == 'cured':
        #         result2 = "A: {}的累计治愈人数为{}。".format(location_list[0][1], number)
        return render_template("result.html", result=post_q,result2=result2)


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)