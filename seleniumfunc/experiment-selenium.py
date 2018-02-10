#selenium自动使用chrome，然后为之后使用PhantomJS做准备
#有时还有bug
#需要添加显式等待代码，能点开的时候就马上点开，不用等加载完，要不然太慢
#等待ajax加载那部分要改，用鼠标拖动到底部那个脚本可能有些问题
#中间还要更换IP和UA
#然后剩下的就是函数和循环了
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
driver = webdriver.Chrome()#打开一个chrome浏览器
driver.get('http://www.okooo.com/jingcai/')#进入这个页面
try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,'欧')))
finally:
  element1 = driver.find_element_by_link_text('欧')#找到所有文字为“欧”的元素组成一个列表
  element1.click()#点击列表中第一个元素


windows = driver.window_handles#得到当前打开的标签页的列表
driver.switch_to_window(windows[1])#换到第二个标签页
try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,'足球日历')))
finally:
  element2 = driver.find_element_by_link_text('足球日历')#找到所有文字为“欧”的元素组成一个列表
  element2.click()#点击足球日历


try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[1]/table/tbody/tr[2]/td[7]/span')))
finally:
  select = Select(driver.find_element_by_id('dateyeah'))#找到选择年份的下拉菜单
  select.select_by_visible_text('2016年')#年份选择2016年
  select.select_by_value('2016')#作用同上，是另一种方法，二者选一即可
  select = Select(driver.find_element_by_id('datemonth'))
  select.select_by_value('3')
  day = driver.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[2]/td[7]/span')#找到日期‘5’，用的是火狐firebug找到的xpath
  day.click()#点击日期


bisailist = driver.find_elements_by_class_name('op')#找到当天所有的比赛的欧赔列表
len(bisailist)#查看当天比赛数量
try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'op')))
finally:
  bisailist[0].click()#打开当天第一场比赛的欧赔


windows = driver.window_handles#得到标签页列表
driver.switch_to_window(windows[2])#把driver转到新打开的那场比赛的标签页上
def contenttomongodb(content,companyname,urlnum):
  global client
  global db
  sucker1 = '(href="/soccer/match/)(.*?)(/odds/change/)(.*?)(/)'
  sucker5 = '(<div class="box"id="an">)(.*?)(<span></span>)'
  sucker6 = '(<a href="/soccer/league/)(.*?)(/schedule/)(.*?/">)(.*?)(</a>)'
  sucker7 = '(<a href="/soccer/match/)(.*?)(/odds/">)(.*?)(vs)(.*?)(</a>)'
  cid = re.search(sucker1,content).group(4)
  saishi = re.search(sucker6,content).group(5)
  zhudui = re.search(sucker7,content).group(4)
  kedui = re.search(sucker7,content).group(6)
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
      record['saishi'] = saishi
      record['cid'] = cid
      record['zhudui'] = zhudui
      record['kedui'] = kedui
      record['companyname'] = companyname
      record['time'] = s2[i][0]
      record['left-time'] = s2[i][1]
      record['peilv'] = [s2[i][2],s2[i][3],s2[i][4]]
      record['gailv'] = [s2[i][5],s2[i][6],s2[i][7]]
      record['kailizhishu'] = [s2[i][8],s2[i][9],s2[i][10]]
      record['fanhuanlv'] = s2[i][11]
      collection.insert(record)


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
  companynamelist = list()
  source = driver.page_source
  sucker3 = '(<a href="/soccer/match/)(.*?)(/odds/change/)(.*?/">)(.*?)(</a>)'
  companylist = re.findall(sucker3,source)
  for i in range(0,len(companylist)):
      companynamelist.append(companylist[i][4])
  #以上就得到了当场比赛开赔公司名称的名单
  for i in range(0,len(companynamelist)):
      element = driver.find_element_by_id('an')
      element.click()
      element = driver.find_element_by_link_text(companynamelist[i])
      element.click()
      content = driver.page_source
      contenttomongodb(content,companynamelist[i],urlnum)
      print(companynamelist[i])
  #driver.close()
  #driver.switch_to_window(windows[2])#让driver回到单个比赛页面
  #driver.close()#都爬完了，把那场比赛关掉就好了


def dangtianbisai(driver):


danchangbisai(driver)
end = time.time()
print(end-start)
