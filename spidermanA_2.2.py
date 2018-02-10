#本版本每次网页请求都使用ip池中不同的ip，以及UA池中不同的UA
#此程序用来爬A数据集，即所有公司，所有赛事的所有初赔和终赔
#此爬虫程序用的是spiderman2.2版本
#直接从网页爬取有些网站会拒绝urllib反复请求，所以用requests库
#用同一个ip频繁请求同一个网页时会被服务器屏蔽
#这个程序还是能用的，但是有的时候不稳定，可能需要频繁更换代理ip
#频繁换ip也不行
#让循环之内有0.5秒的间隔也不行，真是他妈的烂透了！！！
#建立起一个UA池，让每次请求拥有的UA随机分配。以此来防止UA限制。但好像还是没什么卵用，好像每天中午都不太行，不知道是不是时间的原因。
#最后一次尝试，就是把协程并发改成每隔0.1秒发一个,然后pagetotxt内部请求的间隔是0.1到0.15之间的随机数
#现在终于可行了，当前代码下，漏爬率率大概1.33%，每秒爬出3个文件，每100文件换一个ip地址，每个网页请求会在一个拥有586个UA池中随机选取一个UA。
#同时每100个任务提取5个ip建立ip池，随机更换ip进行请求，避免被封得太厉害
#就现在的观察，漏爬率可能与换ip频繁程度有关，每150个文件换一个ip，漏爬率为5%。
#睡眠时间与漏爬率也可能有关，可能睡眠时间越短，漏爬率越高。
#2.2终于成功了，但是还有改进空间，因为看起来爬成率好像挺高，那么也就是说，只要准备出几百个有效的ip池，然后几百个UA的UA池，做轮流循环，保证两对相同的IP和UA出现的时间足够长，或许就能越过网站反爬。
#不过是不是这个原理，可能还要等到明天上午的观察再说
#2.3版本就是精简化，高速化，独享动态每天可以提取1000个ip，每个ip可以用2到3天，如果对方服务器条件允许，就可以以极高的速度提取。
#下一步是做网页监控，即时更新数据集

from gevent import monkey; monkey.patch_all()
import requests
import urllib.request
import re 
import gevent
import time
import random#导入随机数模块 
start = time.time()
def getiplist():
  ipname = requests.get('http://www.xdaili.cn/ipagent/privateProxy/applyStaticProxy?count=1&spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1').content#从动态混拨API接口
  ipname = str(ipname)
  ippool = re.findall('(.*?)(\d.*?)(\\\\r\\\\n)',ipname)
  iplist = list()
  for i in range(0,len(ippool)):
      iplist.append(ippool[i][1])#得到了IP列表
  return iplist


iplist = getiplist()


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
  print(iplist)


checkip(iplist)
requests.Session().proxies = {"http":"http://" + iplist[random.randint(0,len(iplist)-1)],}#注意这里是len(iplist)-1!!!!!!!

UAcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()

for i in range(0,int(len(UAname))):    
    UAlist.append(UAname[i][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
time.sleep(10)

def pagetotxt(urlnum):
  #先读取主网页
  url1 = 'http://odds.500.com/fenxi/ouzhi-'+str(urlnum)+'.shtml'
  requests.Session().proxies = {"http":"http://"+ iplist[random.randint(0,len(iplist)-1)],}
  originalcontent = requests.get(url1,headers = {'user-agent': UAlist[random.randint(0,585)]}).content
  time.sleep(random.uniform(0.15,0.2))
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
  for i in range(30,300,30):
      url2 = 'http://odds.500.com/fenxi1/ouzhi.php?id='+str(urlnum)+'&ctype=1&start='+str(i)+'&r=1&style=0&guojia=0&chupan=1'
      requests.Session().proxies = {"http":"http://"+ iplist[random.randint(0,len(iplist)-1)],}
      originalcontent2 = requests.get(url2,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#每发出一个请求你都是用不同的UA和ip
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
  address = 'D:\\lottotxt3\\{date_title}.txt'
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


def coroutine(start):
  ge = list()
  for i in range(0,100):
      ge.append(gevent.spawn(pagetotxt,start))
      start = start + 1
  for i in range(0,100):
      ge[i].join()
      time.sleep(random.uniform(0.01,0.1))
      gevent.sleep(0)


for i in range(399250,700000,100):
    try:
      iplist = getiplist()
      checkip(iplist)
      requests.Session().proxies = {"http":"http://"+iplist[random.randint(0,len(iplist)-1)],}#使用代理ip
    except Exception as e:
      time.sleep(10)
      try:
        iplist = getiplist()
        checkip(iplist)
        requests.Session().proxies = {"http":"http://"+iplist[random.randint(0,len(iplist)-1)],}#使用代理ip
      except Exception as e:
        break   
    coroutine(i)
    print('mit IP:'+str(iplist))
    time.sleep(random.uniform(0.1,0.15))



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))

