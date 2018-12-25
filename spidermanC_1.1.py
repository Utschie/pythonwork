#此版本是spidermanC1.1版本
#由于该程序总共要提出近8000多万个请求，为越过对方网站的反爬机制，不再采用原来的简单单页面遍历方式
#取而代之的是将40万+个fid和437个cid随机组合成对，构成请求参数池
#然后在请求参数池中随机抽取一个提交请求写入数据库
#每写入一个数据就在请求参数池中去掉那个参数对，直到参数池用尽为止
#但是这个版本依然有缺陷，因为这个版本依然是在同一个页面请求许多php，只不过是随机的而已
#所以接下来的版本要改成在多个页面随机请求php
from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
from pymongo import MongoClient
start = time.time()
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


#checkip(ippool)
#获得CID池
with open('D:\lottotxtB\CID.txt') as f:
  CIDtxt = f.read()


tiqu = re.findall('(\()(.*?)(\))',CIDtxt)
CIDlist = list()
for i in range(0,len(tiqu)):
  CIDlist.append(tiqu[i][1])


client = MongoClient()
#用字典创建变量列表，这样就可以批量命名变量了
#创建数据库lottotxtC
db = client.lottotxtC
#创建数据集，相当于关系型数据库里的表
def seriestoMongoDB(urlnum):
  global client
  global db
  collection = db[str(urlnum)]
  for cid in CIDlist:
        try:
          time.sleep(1)
          requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
          url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+str(urlnum)+'&'+'cid='+cid[1:cid.find(',')-1]
          originalcontent = requests.get(url,headers = {'user-agent': UAlist[random.randint(0,585)]}).content
          content = str(originalcontent)
          if content == "b'\\r\\n\\r\\n\\r\\n[]'":
              continue
          sucker1 = '(b\\\'\\\\r\\\\n\\\\r\\\\n\\\\r\\\\n\[)(.*?)(\]\\\')'
          originalserieslist = re.search(sucker1,content).group(2)
          sucker2 = '(\[)(.*?)(\])'
          serieslist = re.findall(sucker2,originalserieslist)
          series = list()
        except Exception as e:
          continue
      for y in range(0,len(serieslist)):
          series.append(serieslist[y][1])
      for z in range(0,len(series)):
          seriesdict = {}
          seriesdict['ID'] = urlnum
          seriesdict['cid'] = cid[1:cid.find(',')-1]
          seriesdict['bocaicompany'] = cid[cid.find(',')+3:len(cid)-1]
          seriesdict['time'] =  re.search('(\")(.*?)(\")',series[z]).group(2)
          peilv_fanhuanlv = series[z][0:series[z].find('"')]
          peilv_fanhuanlv = re.findall('(.*?)(\,)',peilv_fanhuanlv)
          peilv_fanhuanlvlist = list()
          for i in range(0,4):
              peilv_fanhuanlvlist.append(peilv_fanhuanlv[i][0])
          finalpeilv_fanhuanlv = list(map(float,peilv_fanhuanlvlist))
          seriesdict['peilv_fanhuanlv'] = finalpeilv_fanhuanlv
          collection.insert(seriesdict)
      print(cid+'OK')
      

#def coroutine(start):
#  ge = list()
#  for i in range(start,start+150):
#    ge.append(gevent.spawn(seriestoMongoDB,i))
#  gevent.joinall(ge)
#  print('task'+str(start)+'-'+str(start+150)+'finished')
def taskdividing(urlnum):
  #首先让150个fid和437个cid两两搭对，共形成65550个fid_cid对儿
  fid_cidlist = list(str(a) +'_' +b for a in range(urlnum,urlnum+150) for b in CIDlist)
  for fid_cid in fid_cidlist:
      randomnum = random.randint(0,len(fid_cidlist)-1)#设定一个随机“指针”
      tin = fid_cidlist[randomnum]
      url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[8:tin.find(',')-1]
      del fid_cidlist[randomnum]#把刚刚用过的那个fid_cid对儿从池子里去掉


for i in range(250000,250600):
    seriestoMongoDB(i)
    print('Task'+str(i)+'-'+'Task'+str(i+149)+'finished') 



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))


