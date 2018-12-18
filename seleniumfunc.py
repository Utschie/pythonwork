#由于要打开好几层的页面，所以决定，每一层页面的操作都用一个函数表示，便于编写与修改
#danchangbisai函数中，同时打开，同时请求的协程部分可能需要考虑爬取频率
#由于开网页和爬数据分别用协程也并没有很快，所以决定就用原来的就可以了

from selenium import webdriver
from selenium.webdriver.support.ui import Select#用来搞下拉列表
from selenium.webdriver.common.by import By#用来添加显示等待
from selenium.webdriver.support.ui import WebDriverWait#用来添加显示等待
from selenium.webdriver.support import expected_conditions as EC#用来添加显示等待
from gevent import monkey; monkey.patch_all()
import re 
import gevent
import time
import random#导入随机数模块 
from pymongo import MongoClient
import os#用来获取文件名列表
import chardet
from bs4 import BeautifulSoup
import requests
start = time.time()
client = MongoClient()
db = client.lottotxtC
#首先是把数据从content中写入MongoDB中的函数，即在具体供公司赔率页面上的操作
def contenttomongodb(content):
  global client
  global db
  sucker1 = '(href="/soccer/match/)(.*?)(/odds/change/)(.*?)(/)'
  sucker5 = '(<div class="box"  id="an">)(.*?)(<span></span>)'
  urlnum = re.search(sucker1,content).group(2)
  cid = re.search(sucker1,content).group(4)
  companyname = re.search(sucker5,content).group(2)
  collection = db[urlnum]
  soup = BeautifulSoup(content,"lxml")
  table = soup.table
  tr = table.find_all('tr')
  del tr[0],tr[0],tr[1]
  s1 = list()
  for x in range(0,len(tr)):
      s1.append(str(tr[x]))
  sucker2 = '(>)(.*?)(<)'
  s2 = list()
  for u in range(0,len(s1)): 
      uu = re.findall(sucker2,s1[u])
      uuu = list()
      for w in range(0,len(uu)):
          uuu.append(uu[w][1])  
      while '' in uuu:
          uuu.remove('')#去除列表中的空元素
      for i in range(0,len(uuu)):
          if uuu[i][-1] == '↑':#去除列表中的箭头们
              uuu[i] = uuu[i][:-1]
          elif uuu[i][-1] == '↓':
              uuu[i] = uuu[i][:-1] 
      for i in range(2,len(uuu)):
          uuu[i] = float(uuu[i])
      s2.append(uuu) 
  for i in range(0,len(s2)):
      record = {}
      record['cid'] = cid
      record['companyname'] = companyname
      record['time'] = s2[i][0]
      record['left-time'] = s2[i][1]
      record['peilv'] = [s2[i][2],s2[i][3],s2[i][4]]
      record['gailv'] = [s2[i][5],s2[i][6],s2[i][7]]
      record['kailizhishu'] = [s2[i][8],s2[i][9],s2[i][10]]
      record['fanhuanlv'] = s2[i][11]
      collection.insert(record)


#下面是一个开网页的函数，在单场比赛函数中会用到，因为要协程
def kaiwangye(driver,i):
  xpath = '/html/body/div[6]/table/tbody/tr['+str(i)+']/td[6]/a/span'
  element = driver.find_element_by_xpath(xpath)
  element.click()



#下面是一个发请求爬数据的函数，在单场比赛函数中会用到，因为要协程
def faqingqiu(urlnum,cid):
  url = 'http://www.okooo.com/soccer/match/'+str(urlnum)+'/odds/change/'+str(cid)+'/'
  content = requests.get(url).content
  content = content.decode('gb18030')
  content = str(content)
  contenttomongodb(content)


#把单场比赛所有公司的赔率都同时用contenttomongodb函数过一遍，即同时打开所有公司赔率页面，同时
def danchangbisai(driver):#此时的driver在单个比赛页面上
  #先得到urlnum
  sucker4 = '(http://www.okooo.com/soccer/match/)(.*?)(/odds/)'
  urlnum = re.search(sucker4,driver.current_url).group(2)
  #先让driver到单个公司赔率页面找到长长的公司名单
  try:
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')))
  finally:
    company = driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')#如果向下滑动鼠标,这个xpath就可能有问题,另外也并不是所有的比赛都有威廉希尔开盘
    company.click()#点开它
  windows = driver.window_handles#得到标签页列表
  driver.switch_to_window(windows[3])#把driver转到赔率变化的那个标签页上
  #companynamelist = list()
  cidlist = list()
  source = driver.page_source
  sucker3 = '(<a href=")(/soccer/match/)(.*?)(/odds/change/)(.*?)(/)(.*?)(</a>)'
  companylist = re.findall(sucker3,source)
  for i in range(0,len(companylist)):
      #companynamelist.append(companylist[i][6])
      cidlist.append(companylist[i][4])
  #以上就得到了当场比赛开赔公司名称的名单,cid名单
  driver.close()#关掉打开的那个公司赔率页面
  driver.switch_to_window(windows[2])#让driver回到单个比赛页面
    #首先要下拉鼠标直至所有的公司都加载了出来
  element = driver.find_element_by_id('goDown')
  element.click()
  element = driver.find_element_by_id('cusFloatObj')
  element.click()
  #然后再拉上去
  element = driver.find_element_by_id('goUp')
  element.click()
  #接下来同时打开所有的公司赔率页面
  ge1 = list()
  for i in range(2,len(cidlist)+2):
      ge1.append(gevent.spawn(kaiwangye,driver,i))
  gevent.joinall(ge1)
  #把所有的网页打开之后，同时向已打开的网页发出请求，进行爬取
  ge2 = list()
  for i in range(0,len(cidlist)):
      ge2.append(gevent.spawn(faqingqiu,urlnum,cidlist[i]))
  gevent.joinall(ge2)
  #最后把所有新打开的网页都关闭
  windows = driver.window_handles#得到标签页列表
  for i in range(3,len(windows)):
      driver.switch_to_window(windows[i])
      driver.close()
  #让driver回到单个比赛的页面
  driver.switch_to_window(windows[2])
  driver.close()#都爬完了，把那场比赛关掉就好了


#然后是把当天的所有比赛都用danchangbisai函数过一遍，但是这个做不到同时
def dangtianbisai(driver):
  initial = driver.current_window_handle
  bisailist = driver.find_elements_by_class_name('op')#找到当天所有的比赛的欧赔列表
  for i in range(0,len(bisailist)):
      try:
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'op')))
      finally:
        bisailist[i].click()#打开当天第一场比赛的欧赔
        windows = driver.window_handles#得到标签页列表
        driver.switch_to_window(windows[2])#把driver转到新打开的那场比赛的标签页上
        try:
          element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')))
        finally:
          company = driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')#如果向下滑动鼠标,这个xpath就可能有问题,另外也并不是所有的比赛都有威廉希尔开盘
          company.click()#点开它
          windows = driver.window_handles#得到标签页列表
          driver.close()
          driver.switch_to_window(windows[3])#把driver转到赔率变化的那个标签页上
          danchangbisai(driver)
          driver.switch_to_window(initial)#抓完一场比赛后让driver再回到原来的上面
          

#然后就是一个又一个地变换日期
def bianhuanriqi(driver):
  





