#爬取每场比赛每个公司的变盘数据
#总共会爬取大约8千万个文件
#而且这样会提出8000万个requests，可能会很浪费时间
#可以先做一下实验，根据实验结果再改
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
  fid_cidlist = list(str(a) +'_' +b for a in range(urlnum,urlnum+1) for b in CIDlist)
  for i in range(0,65550):
        try:
          time.sleep(1)
          randomnum = random.randint(0,len(fid_cidlist)-1)#设定一个随机“指针”
          tin = fid_cidlist[randomnum]
          requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
          url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[8:tin.find(',')-1]
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
      del fid_cidlist[randomnum]
      print(cid+'OK')
      

#def coroutine(start):
#  ge = list()
#  for i in range(start,start+150):
#    ge.append(gevent.spawn(seriestoMongoDB,i))
#  gevent.joinall(ge)
#  print('task'+str(start)+'-'+str(start+150)+'finished')


for urlnum in range(250000,250600):
    seriestoMongoDB(urlnum)
    print('Task'+str(urlnum)+'-'+'Task'+str(i+149)+'finished') 



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))












