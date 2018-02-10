#直接从网页爬取有些网站会拒绝urllib反复请求，所以用requests库
import requests 
import chardet 
import re 
from multiprocessing import Pool
import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Group 
import time 
start = time.time()
def pagetotxt(urlnum):
  #先读取主网页
  url1 = 'http://odds.500.com/fenxi/ouzhi-'+str(urlnum)+'.shtml'
  #print(url1)
  originalcontent = requests.get(url1).content
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
      originalcontent2 = requests.get(url2).content
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
  address = address.format(date_title = date+'_'+title)
  with open(address,"w") as f:
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



ge = list()
for i in range(250000,250150):
  ge.append(gevent.spawn(pagetotxt,i))

  
gevent.joinall(ge)


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))

