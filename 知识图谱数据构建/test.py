from py2neo import Graph
_graph = Graph(
        host='127.0.0.1', # neo4j 搭载服务器的ip地址
        http_port='7687', # neo4j 服务器监听的端口号
        user='neo4j', # 数据库user name，如果没有更改过，应该是neo4j
        password='AHyySZ0323' # 自己设定的密码
        )
#
# # 上海的累计确诊人数是多少？
# # pipe1 = ['累计确诊','当前确诊']
# cur = _graph.run('match(c:cured) where c.name="美国" return c.number;')
# data = cur.data()
# # print(data[0]['c.number'])
#
# # nodes = _graph.nodes
# # # n=nodes.match("province",name='上海')
# # # for i in n:
# # #     print(i)
#
# # 查询语句
# sql = []
# # 1. 查询国内某省市的累计确诊人数
# # if question_type == 'domestic_confirmed':
# sql = ["match(m:confirmed) where m.continent='亚洲' return m.country,m.number;"]
# # cur = _graph.run(sql[0])
# # data = cur.data()
# # country_list={}
# # for i in range(len(data)):
# #         if data[i]['m.country'] not in country_list:
# #                 country_list[data[i]['m.country']] = int(data[i]['m.number'])
# # country_list = list(country_list.items())
# # country_list.sort(key = lambda x:x[1],reverse=True)
# # for i in range(1):
# #         name,number=country_list[i]

# sql = ["match(m:province) where m.country='中国' return m.name;"]
# cur = _graph.run(sql[0])
# data = cur.data()
# province_list=[]
# for i in range(len(data)):
#         province_list.append(data[i]['m.name'])
# sum = 0
# for i in range(len(province_list)):
#         sql = ["match(m:cured) where m.province='{}' return m.number".format(province_list[i])]
#         cur = _graph.run(sql[0])
#         data = cur.data()
#         num = data[0]['m.number']
#         sum += num
# print(sum)
# for i in range(len(data)):
#         if data[i]['m.name'] not in province_list:
#                 province_list[data[i]['m.name']] = int(data[i]['m.number'])
# country_list = list(country_list.items())
# country_list.sort(key = lambda x:x[1],reverse=True)

import jieba
word = jieba.cut('委内瑞拉的政治')
for w in word:
        print(w)