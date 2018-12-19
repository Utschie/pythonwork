import urllib.request#加载urllib.request用来提取网页
import chardet#加载chardet用来查看网页代码以及给网页转码
import re#加载re用来使用正则表达式
from bs4 import BeautifulSoup#加载bs4包，并将其命名为BeautifulSoup
#首先得到一个包含了网页代码的对象
#首先把网页保存下来，使之成为本地的一个htm文件
#然后利用python提取该文件的网页代码
#检测编码方式并解码
#如下所示
originalcontent = urllib.request.urlopen('file:///D:/lottowebpage/odds.500.com/fenxi/ouzhi-519016.shtml').read()
#originalcontent就是网页的代码
chardet.detect(originalcontent)#检测网页编码
content = originalcontent.decode('gb18030')
#decodecontent就是解码后的网页源码，可以显示中文
content #这就显示出网页代码了
#然后用BeautifulSoup来读取包含网页代码的对象
date = re.search('(<p class="game_time">比赛时间)(.*?)(</p>)',content).group(2)
date = date[0:10]
rawtitle = re.search('(<title>)(.*?)(-百家欧赔-500彩票网</title>)',content)
title = rawtitle.group(2)
title = re.search('(.*?)(\(.*?\))',title).group(1)
soup = BeautifulSoup(content,"lxml")#将content的内容用BeautifulSoup读入soup
#其中“lxml”是最好的解析代码的解析器，写上比较好
#找到网页中所有的博彩公司的名字，得到一个对象，如下
company = soup.find_all(class_ = "tb_plgs")#找到soup中所有包含对象class属性为tb_plgs的标签
company = str(company)#将company对象转换成字符串
#下面用正则表达式提取符合条件的第一个字符串
sucker1 = '("display:;">)(.*?)(</span)'#设定正则表达式的模式，‘.*’表示任意数量的所有字符，‘？’表示非贪婪匹配
#所以‘.*?’就表示取‘"dispaly:;">’和‘span’之间的最小字符串
#括号是为了分组
rawresult = re.findall(sucker1,company)#用re.search找到所有符合条件的字符串
rawresult#查看匹配到的字符串，是一个列表
rawresult[3][1]#3号元组的1号字符串，即bet365
finalresult = list()#必须先定义finalresult为一个列表对象
for i in range(0,len(rawresult)):
    finalresult.append(rawresult[i][1])#在finalresult后面添加新对象

bocaicompany = str(finalresult)
#下面找出所有的赔率，返奖率，凯利指数等数据
#先找赔率的
bifen = re.search('(<strong>)(.*?)(</strong>)',content).group(2)
sucker2 = '("cursor:pointer" >)(.*?)(</td>)'#提取规则的正则表达式
type(content)#看得出content本身就是字符串
number = re.findall(sucker2,content)#提取出来成一个列表
len(number)#查看列表长度，为180
number[3][1]#number3号元组的1号元素，为2.30
type(number[3][1])#类型为字符串
peilv = list()
for i in range(0,int(len(number))):
    peilv.append(number[i][1])

type(peilv)
len(peilv)
#检验一下数据类型和长度，赔率列表就算做好了
#接着找即时概率的
sucker2 = '(<td row="1".*? >)(.*?%)(</td>)'
number = re.findall(sucker2,content)
len(number)
jishigailv = list()
for i in range(0,int(len(number))):
    jishigailv.append(number[i][1])

type(jishigailv)
len(jishigailv)
#接着找返还率的
sucker3 = '(<td row="1">)(.*?%)(</td>)'
number = re.findall(sucker3,content)
len(number)
fanhuanlv = list()
for i in range(0,int(len(number))):
    fanhuanlv.append(number[i][1])

type(fanhuanlv)
len(fanhuanlv)
#接着找即时凯利指数的
sucker4 = '(<td row="1" class="".*?>)(.*?)(</td>)'
number = re.findall(sucker4,content)
len(number)
jishikailiindex = list()
for i in range(0,int(len(number))):
    jishikailiindex.append(number[i][1])

type(jishikailiindex)
len(jishikailiindex)
#下面是输出成csv文件
peilv = str(peilv)
jishigailv = str(jishigailv)
fanhuanlv = str(fanhuanlv)
jishikailiindex = str(jishikailiindex)
print(peilv)
print(jishigailv)
print(fanhuanlv)
print(jishikailiindex)
print(title)
print(date)
print(bifen)
address = 'D:\\pythonlabor\\{date_title}.txt'
address = address.format(date_title = date+'_'+title)
print(address)
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


