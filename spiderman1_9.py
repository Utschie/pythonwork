#重大喜讯！！！！！！！
#重大喜讯！！！！！！！
#重大喜讯！！！！！！！
#重要的事情说三遍
#1.9版本用的是最普通的办法，即同时打开多个python(anaconda)窗口
#然后手动分割任务成三份后，同时放到这三个窗口里去跑，实现了真正的多进程！！！！
#最终完成时间52秒！！！
#52秒！！！！！！


import urllib.request#加载urllib.request用来提取网页
import chardet#加载chardet用来查看网页代码以及给网页转码
import re#加载re用来使用正则表达式
from bs4 import BeautifulSoup#加载bs4包，并将其命名为BeautifulSoup
import time

start = time.time()
def pagetotxt(url):
  #首先得到一个包含了网页代码的对象
    #首先把网页保存下来，使之成为本地的一个htm文件
    #然后利用python提取该文件的网页代码
    #检测编码方式并解码
    #如下所示
  originalcontent = urllib.request.urlopen(url).read()
    #originalcontent就是网页的代码
  content = originalcontent.decode('gb18030')
    #decodecontent就是解码后的网页源码，可以显示中文
  content #这就显示出网页代码了
  #然后用BeautifulSoup来读取包含网页代码的对象
  date = re.search('(<p class="game_time">比赛时间)(.*?)(</p>)',content).group(2)
  date = date[0:10]
  rawtitle = re.search('(<title>)(.*?)(-百家欧赔-500彩票网</title>)',content)
  title = rawtitle.group(2)
  title = re.sub('/','',title)
  title = re.sub('\d','',title)
  saishi = re.search('(\()(.*?)(\))',title).group(2)
  soup = BeautifulSoup(content,"lxml")#将content的内容用BeautifulSoup读入soup
  #本来“lxml”是最好的解析代码的解析器，但是python3.6和3.5都用不了，所以1.9版本中去掉了
  #找到网页中所有的博彩公司的名字，得到一个对象，如下
  company = soup.find_all(class_ = "tb_plgs")#找到soup中所有包含对象class属性为tb_plgs的标签
  company = str(company)#将company对象转换成字符串
  #下面用正则表达式提取符合条件的第一个字符串
  sucker1 = '("display:;">)(.*?)(</span)'#设定正则表达式的模式，‘.*’表示任意数量的所有字符，‘？’表示非贪婪匹配
  #所以‘.*?’就表示取‘"dispaly:;">’和‘span’之间的最小字符串
  #括号是为了分组
  rawresult = re.findall(sucker1,company)#用re.search找到所有符合条件的字符串
  rawresult#查看匹配到的字符串，是一个列表
  finalresult = list()#必须先定义finalresult为一个列表对象
  for i in range(0,len(rawresult)):
      finalresult.append(rawresult[i][1])#在finalresult后面添加新对象
  
  bocaicompany = str(finalresult)
  bifen = re.search('(<strong>)(.*?)(</strong>)',content).group(2)
  #下面找出所有的赔率，返奖率，凯利指数等数据
  #先找赔率的
  sucker2 = '("cursor:pointer" >)(.*?)(</td>)'#提取规则的正则表达式
  number = re.findall(sucker2,content)#提取出来成一个列表
  number[3][1]#number3号元组的1号元素，为2.30
  peilv = list()
  for i in range(0,int(len(number))):
      peilv.append(number[i][1])
  
  #检验一下数据类型和长度，赔率列表就算做好了
  #接着找即时概率的
  sucker2 = '(<td row="1".*? >)(.*?%)(</td>)'
  number = re.findall(sucker2,content)
  jishigailv = list()
  for i in range(0,int(len(number))):
      jishigailv.append(number[i][1])
  
  #接着找返还率的
  sucker3 = '(<td row="1">)(.*?%)(</td>)'
  number = re.findall(sucker3,content)
  fanhuanlv = list()
  for i in range(0,int(len(number))):
      fanhuanlv.append(number[i][1])
  
  #接着找即时凯利指数的
  sucker4 = '(<td row="1" class="".*?>)(.*?)(</td>)'
  number = re.findall(sucker4,content)
  jishikailiindex = list()
  for i in range(0,int(len(number))):
      jishikailiindex.append(number[i][1])
  
  #下面是输出成csv文件
  peilv = str(peilv)
  jishigailv = str(jishigailv)
  fanhuanlv = str(fanhuanlv)
  jishikailiindex = str(jishikailiindex)
  #print(bocaicompany)
  #print(peilv)
  #print(jishigailv)
  #print(fanhuanlv)
  #print(jishikailiindex)
  #print(title)
  #print(date)
  #print(bifen)
  address = 'D:\\pythonlabor2\\{date_title}.txt'
  address = address.format(date_title = date+'_'+title)
  #print(address)
  with open(address,"w") as f:
    f.write(bocaicompany)
    f.write('\n')
    f.write('\n')
    f.write(date)
    f.write('\n')
    f.write('\n')
    f.write(title)
    f.write('\n')
    f.write('\n')
    f.write(saishi)
    f.write('\n')
    f.write('\n')
    f.write(bifen)
    f.write('\n')
    f.write('\n')
    f.write(peilv)
    f.write('\n')
    f.write('\n')
    f.write(jishigailv)
    f.write('\n')
    f.write('\n')
    f.write(fanhuanlv)
    f.write('\n')
    f.write('\n')
    f.write(jishikailiindex)
    f.write('\n')
    f.write('\n')


for i in range(250000,334549):
    url = 'file:///D:/lottowebpage/odds.500.com/fenxi/ouzhi-{n}.shtml'
    url = url.format(n=i)
    try:
      pagetotxt(url)
      print(i)
    except Exception as e:
      continue


end = time.time()
print('MISSION COMPLETED. I AM THE SPIDERMAN')
print(str(end-start))
