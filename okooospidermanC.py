#500彩票网的服务器过载能力有限，转而尝试澳客网的！！！
from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
from pymongo import MongoClient
import os#用来获取文件名列表
import chardet
startpoint = time.time()
with open('D:\\ippool.txt','r') as f:
  ippool = f.readlines()#注意是readlines而不是readline，前者是一次性读取所有行，后者是读取一行


for i in range(0,len(ippool)):
    ippool[i] = re.search('(.*?)(\\n)',ippool[i]).group(1)

print(ippool)#打印出ip池

#接下来获取UA池
UAcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()

for i in range(0,int(len(UAname))):    
    UAlist.append(UAname[i][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
def checkip(iplist):
  for i in range(0,len(iplist)):  
      try:
        requests.get('https://www.google.de/',proxies = {"http":"http://"+ iplist[i]})
      except:
        iplist[i] = ''
      else:
        continue
  while '' in iplist:
    iplist.remove('')
  print(str(len(iplist)))


checkip(ippool)
with open('D:\lottotxtB\CID.txt') as f:
  CIDtxt = f.read()


tiqu = re.findall('(\()(.*?)(\),)',CIDtxt)
CIDlist = list()
for i in range(0,len(tiqu)):
  CIDlist.append(tiqu[i][1])


client = MongoClient()
#用字典创建变量列表，这样就可以批量命名变量了
#创建数据库lottotxtC
db = client.lottotxtC
#创建数据集，相当于关系型数据库里的表

path = 'D:\lottotxtA'
names = os.listdir(path)#names是一个包含了path下所有文件的文件名的列表，每个文件名都是字符串

def webtomongodb(tin,urlnum):
  global client
  global db
  collection = db[str(urlnum)]
  fid = tin[]
  cid = tin[]
  requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
  url = 'http://www.okooo.com/soccer/match/'+fid+'/odds/change/'+cid+'/'
  qingqiu = requests.get(url,headers = {'user-agent': UAlist[random.randint(0,585)]})
  print(str(tin)+str(qingqiu))
  originalcontent = qingqiu.content
  content = str(originalcontent)
  content = content.decode('gb18030')
  sucker1 = '(<td class="noborder bright">)(.*?)(</td>)'
  timelist = re.findall(sucker1,content)
  sucker2 = 