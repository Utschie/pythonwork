import urllib.request#加载urllib.request用来提取网页
import chardet#加载chardet用来查看网页代码以及给网页转码
import re#加载re用来使用正则表达式
import pandas as pd#加载pandas来使用pandas提取表格

originalcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/expri-page.htm').read()
  #originalcontent就是网页的代码
content = originalcontent.decode('gb18030')
number = pd.read_html(content)
pd.set_option('max_rows',2000)#设定最大行数
number[10]#显示number中第十个元素
