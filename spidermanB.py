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
  #print(str(len(iplist)))




checkip(ippool)
def seriestotxt(urlnum):
  for i in range(1,CID总数):
      url = 'http://odds.500.com/fenxi1/json/ouzhi.php?fid='+str(urlnum)+'&'+'cid='+str(i)
      originalcontent = request.get(url).content 
      content = str(originalcontent)
      sucker = '(b\\\'\\\\r\\\\n\\\\r\\\\n\\\\r\\\\n\[)(.*?)(\]\\\')'
      series = re.search(sucker,content).group(2)
      address = 'D:\\lottotxtA\\{urlnum_cid}.txt'
      address = address.format(date_title = str(urlnum)+'_'+str(i))
      with open(address,"at") as f:
        f.write(str(urlnum))
        f.write('\n')
        f.write(str(i))
        f.write('\n')
        f.write(series)
        f.write('\n')



def coroutine(start):
  ge = list()
  for i in range(start,start+150):
    ge.append(gevent.spawn(seriestotxt,i))
  gevent.joinall(ge)
  print('task'+str(start)+'-'+str(start+150)+'finished')


for i in range(635050,700000,150):
    coprocess(i)
    print('Task'+str(i)+'-'+'Task'+str(i+149)+'finished') 



print('All subprocess done')


end = time.time()
print('MISSION COMPLETED.用时：')
print(str(end-start))












