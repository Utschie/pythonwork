#本版本是spidermanA2.x最后一代版本
#原理是准备一个1121个ip高匿IP池和586个UA的UA池
#每次请求都用随机的IP和UA配对儿，中间不睡眠，全速爬取数据。
#每组协程任务也就150个，再多会受对方服务器限制
#最快速度为每秒10个文件,不能再快了，再快就被服务器拒绝了
#经试验不能多开，说明服务器对请求速度还是有限制
#抓取率已经很好了，看缘分，也有因为超速而被服务器拒绝的情况出现
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


checkip(ippool)
#经检验全部有效
def pagetotxt(urlnum):
  #先读取主网页
  url1 = 'http://odds.500.com/fenxi/ouzhi-'+str(urlnum)+'.shtml'
  #print(url1)
  requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
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
      requests.Session().proxies = {"http":"http://"+ ippool[random.randint(0,len(ippool)-1)],}
      originalcontent2 = requests.get(url2,headers = {'user-agent': UAlist[random.randint(0,585)]}).content#每发出一个请求你都是用不同的UA
      #time.sleep(random.uniform(0.01,0.03))
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
  address = 'D:\\lottotxtA\\{date_title}.txt'
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


for i in range(635050,700000,150):
    coprocess(i)
    print('Task'+str(i)+'-'+'Task'+str(i+149)+'finished') 



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))


