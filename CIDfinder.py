#提取2016年到2017年的博彩公司的名字和cid对应表
#运行了6个小时，共473个cid
from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
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

CID = list()
#经检验全部有效
def CIDfinder(urlnum):
  global CID
  url1 = 'http://odds.500.com/fenxi/ouzhi-'+str(urlnum)+'.shtml'
  #print(url1)
  requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
  originalcontent = requests.get(url1,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#random.randint(0,586)每次都会返回一个不同的0到585之间的随机整数
  content = originalcontent.decode('gb18030')
  sucker1 = '(<tr class=".*?" )(id=")(.*?)(")(.*?)(xls="row">)'
  number = re.findall(sucker1,content)
  idlist = list()
  for i in range(0,len(number)):
      idlist.append(number[i][2])
  sucker2 = '(<td)(.*?)(class="tb_plgs")(.*?)(title=")(.*?)(">)'
  name = re.findall(sucker2,content)
  company = list()
  for i in range(0,len(name)):
      company.append(name[i][5])
  CID1 = list()
  for i in range(0,len(name)):
      q = number[i][2],name[i][5] 
      CID1.append(q)
  CID = CID + CID1
  for i in range(30,300,30):
      url2 = 'http://odds.500.com/fenxi1/ouzhi.php?id='+str(urlnum)+'&ctype=1&start='+str(i)+'&r=1&style=0&guojia=0&chupan=1'
      requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
      originalcontent2 = requests.get(url2,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#每发出一个请求你都是用不同的UA
      #time.sleep(random.uniform(0.01,0.03))
      content2 = originalcontent2.decode('utf-8')
      number2 = re.findall(sucker1,content2)
      idlist2 = list()
      for i in range(0,len(number2)):
          idlist2.append(number2[i][2])
      sucker2 = '(<td)(.*?)(class="tb_plgs")(.*?)(title=")(.*?)(">)'
      name2 = re.findall(sucker2,content2)
      company2 = list()
      for i in range(0,len(name2)):
          company2.append(name2[i][5])
      CID2 = list()
      for i in range(0,len(name2)):
          p = number2[i][2],name2[i][5] 
          CID2.append(p)
      CID = CID + CID2



address = 'D:\\lottotxtB\\CID.txt'
def coprocess(start):
  global CID
  global address
  ge = list()
  for i in range(start,start+150):
    ge.append(gevent.spawn(CIDfinder,i))
  gevent.joinall(ge)
  CID = list(set(CID))
  with open(address,"w") as f:
    f.write(str(CID))
  print('task'+str(start)+'-'+str(start+150)+'finished')


for i in range(250000,700000,150):
    coprocess(i)
    print('Task'+str(i)+'-'+'Task'+str(i+149)+'finished')


CID = list(set(CID))
with open(address,"w") as f:
  f.write(str(CID))



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))

