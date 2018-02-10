#采用动态混拨，10秒可以提取5个ip，校验IP后，建立IP池，然后每个请求在池子中随机更换IP
import requests
import re
ipname = requests.get('http://www.xdaili.cn/ipagent/privateProxy/applyStaticProxy?count=1&spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1').content#从动态混拨API接口
ipname = str(ipname)
ippool = re.findall('(.*?)(\d.*?)(\\\\r\\\\n)',ipname)
iplist = list()
for i in range(0,len(ippool)):
    iplist.append(ippool[i][1])#得到了IP列表


#检验ip是否可用
for i in range(0,len(iplist)):
    requests.get('https://www.google.de/',proxies = {"http":"http://"+ iplist[i]})


#检验完毕后，使用iplist中的元素随机分配ip地址

