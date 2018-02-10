#直接从网页爬取有些网站会拒绝urllib反复请求，所以用requests库
#用同一个ip频繁请求同一个网页时会被服务器屏蔽
#这个程序还是能用的，但是有的时候不稳定，可能需要频繁更换代理ip
#频繁换ip也不行
#让循环之内有0.5秒的间隔也不行，真是他妈的烂透了！！！
#建立起一个UA池，让每次请求拥有的UA随机分配。以此来防止UA限制。但好像还是没什么卵用，好像每天中午都不太行，不知道是不是时间的原因。
#最后一次尝试，就是把协程并发改成每隔0。5到1秒发一个
#我决定开发2.2，改用selenium模拟浏览器环境读取了
import requests
import urllib.request
import chardet 
import re 
from multiprocessing import Pool
import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Group 
import time
import random#导入随机数模块 
start = time.time()
ip = requests.get('http://www.xdaili.cn/ipagent//newExclusive/getIp?spiderId=0a4b8956ad274e579822b533d27f79e1&orderno=DX20177241880pXU3AZ&returnType=1&count=1&machineArea=').content#API接口链接
ip = str(ip)
ip = re.search('(b\')(.*?)(\\\\n\')',ip)[2]
requests.Session().proxies = {"http":"http://"+ip,}#使用代理ip
print(ip)
UAcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for i in range(0,int(len(UAname))):    
    UAlist.append(UAname[i][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
time.sleep(20)
def pagetotxt(urlnum):
  #先读取主网页
  url1 = 'http://odds.500.com/fenxi/ouzhi-'+str(urlnum)+'.shtml'
  #print(url1)
  originalcontent = requests.get(url1,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#random.randint(0,586)每次都会返回一个不同的0到585之间的随机整数
  content = originalcontent.decode('gb18030')
  date = re.search('(<p class="game_time">比赛时间)(.*?)(</p>)',content).group(2)
  date = date[0:10]
  rawtitle = re.search('(<title>)(.*?)(-百家欧赔-500彩票网</title>)',content)
  title = rawtitle.group(2)
  title = re.sub('/','',title)
  title = re.sub('\d','',title)
  saishi = re.search('(\()(.*?)(\))',title).group(2)
  bifen = re.search('(<strong>)(.*?)(</strong>)',content).group(2)
  #接下来提取列表
  sucker1 = '("display:;">)(.*?)(</span)'
  name = re.findall(sucker1,content)
  bocaicompany = list()
  for i in range(0,len(name)):
      bocaicompany.append(name[i][1])
  sucker2 = '("cursor:pointer" >)(.*?)(</td>)'
  number = re.findall(sucker2,content)
  peilv = list()
  for i in range(0,int(len(number))):
      peilv.append(number[i][1])  
  sucker3 = '(<td row="1".*? >)(.*?%)(</td>)'
  number = re.findall(sucker3,content)
  jishigailv = list()
  for i in range(0,int(len(number))):
      jishigailv.append(number[i][1])  
  sucker4 = '(<td row="1">)(.*?%)(</td>)'
  number = re.findall(sucker4,content)
  fanhuanlv = list()
  for i in range(0,int(len(number))):
      fanhuanlv.append(number[i][1])  
  sucker5 = '(<td row="1" class="".*?>)(.*?)(</td>)'
  number = re.findall(sucker5,content)
  jishikailiindex = list()
  for i in range(0,int(len(number))):
      jishikailiindex.append(number[i][1]) 
  #以下是读取动态加载的网页
  #先把代码爬下来为content2
  for i in range(30,300,30):
      #print(str(i))
      url2 = 'http://odds.500.com/fenxi1/ouzhi.php?id='+str(urlnum)+'&ctype=1&start='+str(i)+'&r=1&style=0&guojia=0&chupan=1'
      originalcontent2 = requests.get(url2,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#每发出一个请求你都是用不同的UA
      time.sleep(random.uniform(0.5,1))#随机睡眠防止爬的过快
      content2 = originalcontent2.decode('utf-8')
      #接下来陆续提取bocaicompany2，peilv2，jishigailv2,fanhuanlv2,jishikailiindex2,好消息是加载出的网页提取规则跟主网页是一样的，所以sucker用原来的就行
      name = re.findall(sucker1,content2)
      bocaicompany2 = list()
      for i in range(0,int(len(name))):
          bocaicompany2.append(name[i][1])
      bocaicompany = bocaicompany + bocaicompany2
      number = re.findall(sucker2,content2)
      peilv2 = list()
      for i in range(0,int(len(number))):
          peilv2.append(number[i][1])
      peilv = peilv + peilv2
      number = re.findall(sucker3,content2)
      jishigailv2 = list()
      for i in range(0,int(len(number))):
          jishigailv2.append(number[i][1])
      jishigailv = jishigailv + jishigailv2
      number = re.findall(sucker4,content2)
      fanhuanlv2 = list()
      for i in range(0,int(len(number))):
          fanhuanlv2.append(number[i][1])
      fanhuanlv = fanhuanlv + fanhuanlv2
      number = re.findall(sucker5,content2)
      jishikailiindex2 = list()
      for i in range(0,int(len(number))):
          jishikailiindex2.append(number[i][1]) 
      jishikailiindex = jishikailiindex + jishikailiindex2 
  bocaicompany = str(bocaicompany)
  peilv = str(peilv)
  jishigailv = str(jishigailv)
  fanhuanlv = str(fanhuanlv)
  jishikailiindex = str(jishikailiindex)
  address = 'D:\\lottotxt\\{date_title}.txt'
  address = address.format(date_title = str(urlnum)+'_'+date+'_'+title)
  with open(address,"w") as f:
    f.write('ID')
    f.write('\n')
    f.write(str(urlnum))
    f.write('\n')
    f.write('\n')
    f.write('date')
    f.write('\n')
    f.write(date)
    f.write('\n')
    f.write('\n')
    f.write('title')
    f.write('\n')
    f.write(title)
    f.write('\n')
    f.write('\n')
    f.write('saishi')
    f.write('\n')
    f.write(saishi)
    f.write('\n')
    f.write('\n')
    f.write('bifen')
    f.write('\n')
    f.write(bifen)
    f.write('\n')
    f.write('\n')
    f.write('bocaicompany')
    f.write('\n')
    f.write(bocaicompany)
    f.write('\n')
    f.write('\n')
    f.write('peilv')
    f.write('\n')
    f.write(peilv)
    f.write('\n')
    f.write('\n')
    f.write('jishigailv')
    f.write('\n')
    f.write(jishigailv)
    f.write('\n')
    f.write('\n')
    f.write('fanhuanlv')
    f.write('\n')
    f.write(fanhuanlv)
    f.write('\n')
    f.write('\n')
    f.write('jishikailiindex')
    f.write('\n')
    f.write(jishikailiindex)
    f.write('\n')
    f.write('\n')
  print(str(urlnum))

def coprocess(start):
  ge = list()
  for i in range(start,start+150):
    ge.append(gevent.spawn(pagetotxt,i))
  gevent.joinall(ge)
  print('task'+str(start)+'-'+str(start+150)+'finished')


for i in range(356738,700000,150):
    try:
      ip = requests.get('http://www.xdaili.cn/ipagent//newExclusive/getIp?spiderId=0a4b8956ad274e579822b533d27f79e1&orderno=DX20177241880pXU3AZ&returnType=1&count=1&machineArea=').content#API接口链接
      ip = str(ip)
      ip = re.search('(b\')(.*?)(\\\\n\')',ip)[2]
      requests.Session().proxies = {"http":"http://"+ip,}#使用代理ip
    except Exception as e:
      break    
    coprocess(i)
    print('mit IP:'+ip) 
    time.sleep(15)




print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))

