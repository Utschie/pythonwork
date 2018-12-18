from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
from pymongo import MongoClient
import os#用来获取文件名列表
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





#获得CID池，也就是下面的CIDlist
#虽然这种方式成功了，如果fid是从250000到250150的话，那么这个数据对儿就太多了要65550个，不可能同时请求
with open('D:\lottotxtB\CID.txt') as f:
  CIDtxt = f.read()


tiqu = re.findall('(\()(.*?)(\))',CIDtxt)
CIDlist = list()
for i in range(0,len(tiqu)):
  CIDlist.append(tiqu[i][1])


fid_cidlist = list(str(a) +'_' +b for a in range(250000,250150) for b in CIDlist)
for i in range(0,65550):
    randomnum = random.randint(0,len(fid_cidlist)-1)#设定一个随机“指针”
    tin = fid_cidlist[randomnum]
    url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[8:tin.find(',')-1]
    print(tin)
    del fid_cidlist[randomnum]#把刚刚用过的那个fid_cid对儿从池子里去掉





####################读取目录下文件列表##############################
path = 'D:\lottotxtA'
names = os.listdir(path)#names是一个包含了path下所有文件的文件名的列表，每个文件名都是字符串


##############################以下是协程部分######################################################################
#但是这个地方依然有缺陷，因为这个版本依然是连续在同一个页面请求几十个上百个php，只不过是随机的而已
#所以接下来的版本要改成在多个页面随机请求php





def coroutine(start):
  ge = list()
  CIDlist_act = CIDlist_actual(start)#CIDlist_actual是一个从本地文件中读取到的"有意义的"的CID们
  fid_cidlist = list(str(a) +'_' +b for a in range(start,start+5) for b in CIDlist_act)
  q = len(fid_cidlist)  
  for i in range(0,q):
        randomnum = random.randint(0,len(fid_cidlist)-1)#设定一个随机“指针”
        tin = fid_cidlist[randomnum]
        ge.append(gevent.spawn(seriestoMongoDB,tin))
        del fid_cidlist[randomnum]#把用过的那个fid_cid对儿从池子中去掉
  gevent.joinall(ge)
  print('task'+str(start)+'finished')



############################以下是写入数据库函数部分#######################################################################
#将单个请求下来的php网页写入数据库
def seriestoMongoDB(tin):
  global client
  global db
  global fid_cidlist
  global urlnum
  collection = db[str(urlnum)]
  time.sleep(1)
  requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
  url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[8:tin.find(',')-1]
  originalcontent = requests.get(url,headers = {'user-agent': UAlist[random.randint(0,585)]}).content
  content = str(originalcontent)
  if content == "b'\\r\\n\\r\\n\\r\\n[]'":#这个得改，等将来把CIDlist做成读取为文件中的博彩公司列表时，这个就得改
      continue                            #同上
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
        

####################################taskdividing任务分割函数############################################################
def taskdividing(urlnum):
  #首先让150个fid和437个cid两两搭对，共形成65550个fid_cid对儿
  fid_cidlist = list(str(a) +'_' +b for a in range(urlnum,urlnum+150) for b in CIDlist)
  for fid_cid in fid_cidlist:
      randomnum = random.randint(0,len(fid_cidlist)-1)#设定一个随机“指针”
      tin = fid_cidlist[randomnum]
      url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+tin[0:6]+'&'+'cid='+tin[8:tin.find(',')-1]
      del fid_cidlist[randomnum]#把刚刚用过的那个fid_cid对儿从池子里去掉



################################下面是根据文件创建CIDlist_actual列表的函数#################################################
#因为在用协程进行打包之前，需要先知道具体请求那些博彩公司的变盘，以此来避免重复无意义的请求
def CIDlist_actual(start):
  CIDlist_act = list()
  txt = 'D:\\lottotxtA\\'+ names[start]
  with open(txt,'r') as f:
    h = f.readlines()
  sucker3 = '(\\\')(.*?)(\\\')'
  cl = re.findall(sucker3,h[16])
  for i in range(0,len(cl)):
      CIDlist_act.append(cl[i][1])
  return CIDlist_act
      


















####################################上面的部分未完成###############################################################################
######################################下面是生成有意义请求对儿的过程#########################################################
#由于并不是所有的fid和cid搭配都是有意义的，所以可以从本地找出有意义的请求对儿组成一个列表，这个列表有几千万对儿
#然后每次从这个列表中随机找一对儿，不过这样我猜又会很慢。所以我猜比较快的方法是，将连续的几个页面做一个任务
#然后使每次等待处理的请求对儿不短时间集中在同一个页面，然后每次等待处理的不超过一千个，所以约莫着大约每五个页面是一组
#然后这五个页面约1000个请求，在随机顺序处理，并且是限速处理，这样可能会好一些
