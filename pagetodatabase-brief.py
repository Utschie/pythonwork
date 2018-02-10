#首先得到一个包含了网页代码的对象
  #首先把网页保存下来，使之成为本地的一个htm文件
  #然后利用python提取该文件的网页代码
  #检测编码方式并解码
  #如下所示
import urllib.request#加载urllib.request用来提取网页
import chardet#加载chardet用来查看网页代码以及给网页转码
import re#加载re用来使用正则表达式
originalcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/expri-page.htm').read()
  #originalcontent就是网页的代码
content = originalcontent.decode('gb18030')
  #decodecontent就是解码后的网页源码，可以显示中文

#然后用BeautifulSoup来读取包含网页代码的对象
from bs4 import BeautifulSoup#加载bs4包，并将其命名为BeautifulSoup
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

finalresult = list()#必须先定义finalresult为一个列表对象
for i in range(0,len(rawresult)):
    finalresult.append(rawresult[i][1])#在finalresult后面添加新对象

finalresult#这样所有的博彩公司名称就作为一个列表得到了
