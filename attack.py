#本版本是spidermanC1.3版本
#本版本把协程方式改了一改，把同时间一个协程组发出请求，改为隔一段时间发出请求，用以减少response503,结果好像没什么用。
#其实对面服务器是可以接受同时发出10个请求的，也就是说，任务分块儿应该分成差不多每块儿10个左右的情况
#也就是说，taskdividing函数的num，应该是tasklist的num的20倍，下面继续调试，看看可不可以更快，倍数越小，爬取越快

from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
from pymongo import MongoClient
import os#用来获取文件名列表
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


#checkip(ippool)
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

#从单个文件中提取出有用的CIDlist，参数num是names列表的索引,返回一个列表
def CIDlist_actual(num):
  CIDlist_act = list()
  txt = 'D:\\lottotxtA\\'+ names[num]
  with open(txt,'r') as f:
    h = f.readlines()
  sucker3 = '(\\\')(.*?)(\\\')'
  cl = re.findall(sucker3,h[16])
  for i in range(0,len(cl)):
      CIDlist_act.append(cl[i][1])
  return CIDlist_act

response = str()
#将单个请求下来的php网页写入数据库，参数tin是fclist中的元素,urlnum是数据表的名字
def seriestoMongoDB(tin,urlnum):
  global client
  global db
  global fid_cidlist
  global response
  response = str()
  left = 'D:\\spidermanC_left.txt'
  collection = db[str(urlnum)]
  requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
  url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[tin.rfind('_')+1:]
  qingqiu = requests.get(url,headers = {'user-agent': UAlist[random.randint(0,585)]},)
  response = str(qingqiu)
  print(str(tin)+str(qingqiu))
  originalcontent = qingqiu.content
  content = str(originalcontent)
  sucker1 = '(b\\\'\\\\r\\\\n\\\\r\\\\n\\\\r\\\\n\[)(.*?)(\]\\\')'
  originalserieslist = re.search(sucker1,content).group(2)
  sucker2 = '(\[)(.*?)(\])'
  serieslist = re.findall(sucker2,originalserieslist)
  series = list()
  for y in range(0,len(serieslist)):
      series.append(serieslist[y][1])
  for z in range(0,len(series)):
      seriesdict = {}
      seriesdict['ID'] = urlnum
      seriesdict['cid'] = tin[tin.rfind('_')+1:]
      seriesdict['bocaicompany'] = tin[tin.find('_')+1:tin.rfind('_')]
      seriesdict['time'] =  re.search('(\")(.*?)(\")',series[z]).group(2)
      peilv_fanhuanlv = series[z][0:series[z].find('"')]
      peilv_fanhuanlv = re.findall('(.*?)(\,)',peilv_fanhuanlv)
      peilv_fanhuanlvlist = list()
      for i in range(0,4):
          peilv_fanhuanlvlist.append(peilv_fanhuanlv[i][0])
      finalpeilv_fanhuanlv = list(map(float,peilv_fanhuanlvlist))
      seriesdict['peilv_fanhuanlv'] = finalpeilv_fanhuanlv


#生成tasklist,start指示起始页面(按照names里的索引)，num指示合并多少个页面为一个tasklist
def tasklist(start,num):
  list1 = list()
  for i in range(0,num):
      fid = names[start + i][0:6]
      CIDlist_act = CIDlist_actual(start + i)
      fid_cidlist = list(str(fid) +'_' +b for b in CIDlist_act)
      for p in range(0,len(fid_cidlist)):
          list1.append(fid_cidlist[p])
  return list1


#tasklist合成之后需要随机分成几份传送给协程让它运行,tlist时tasklist，num指示分成几份
def taskdividing(tlist,num):
  t2list = list()
  for i in range(0,len(tlist)):
      t2list.append(tlist[i])
  list2 = list()
  for i in range(0,num):
      list2.append(list())#给list2各个元素设为空列表
  q = len(t2list)
  for i in range(0,q):
      randomnum = random.randint(0,len(t2list)-1)
      list2[random.randint(0,num-1)].append(t2list[randomnum])#分配一个随机的元素到随机的任务里
      del t2list[randomnum]
  return list2


#由于taskdivid[c]中的元素是形为“fid_公司名称”的元素，因此需要一个转化函数将其转化成形为“fid_公司名称_cid”式的元素，才能应用到seriestoMongo函数上
def trantofid_cidlist(tdlist):
  list3 = list()
  for i in range(0,len(tdlist)):
      list3.append(tdlist[i])
  for i in range(0,len(tdlist)):
      for companyname in CIDlist:
          if list3[i][7:] == companyname[companyname.find(',')+3:companyname.find('\'')-1]:
              list3[i] = list3[i] + '_' + companyname[1:companyname.find(',')-1]
          else:
              continue
  return list3




#给协程一个list让它去运行
def coroutine(fclist):
  list4 = fclist
  ge = list()
  q = len(list4)  
  for i in range(0,q):
      randomnum = random.randint(0,len(list4)-1)#设定一个随机“指针”
      tin = list4[randomnum]
      urlnum = int(tin[0:6])
      ge.append(gevent.spawn(seriestoMongoDB,tin,urlnum))
      del list4[randomnum]#把用过的那个fid_cid对儿从池子中去掉
  for i in range(0,len(ge)):
      ge[i].join()
      gevent.sleep(0)






for start in range(0,400000,10):
    tlist = tasklist(start,10)#合并任务
    taskdivid = taskdividing(tlist,20)#分解任务
    for c in range(0,len(taskdivid)):
        coroutine(trantofid_cidlist(taskdivid[c])) 
    print('task' + str(start) + '_' + str(start + 10) + 'finished')


print('All subprocess done')


endpoint = time.time()
print('MISSION COMPLETED.用时：')
print(str(endpoint-startpoint))
