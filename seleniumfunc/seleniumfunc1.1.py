#需要用代理的方式打开chrome
#需要同时开至少30个浏览器窗口进行爬取，每个浏览器窗口所用的ip和UA都不一样
#我觉得我的电脑应该考虑换cpu了，一个chrome窗口占用cpu10%，内存200M，也就是说，对于内存可以开50个没问题，但是对于cpu顶多开8个窗口。
#如果必要应该设置一个自动登录自动识别验证码的程序
from selenium import webdriver
from selenium.webdriver.support.ui import Select#用来搞下拉列表
from selenium.webdriver.common.by import By#用来添加显示等待
from selenium.webdriver.support.ui import WebDriverWait#用来添加显示等待
from selenium.webdriver.support import expected_conditions as EC#用来添加显示等待
from selenium.webdriver.common.keys import Keys#用来实现自动登录
from selenium.webdriver.common.action_chains import ActionChains#用来调出右键菜单
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
import urllib
start = time.time()
client = MongoClient()
db = client.lottotxtC
#老规矩，还是先做ip池和ua池
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
        requests.get('http://www.okooo.com/jingcai/',proxies = {"http":"http://"+ iplist[i]})
      except:
        iplist[i] = ''
      else:
        continue
  while '' in iplist:
    iplist.remove('')
  print(str(len(iplist)))


checkip(ippool)

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
  select.select_by_value('2016')#作用同上，是另一种方法，二者选一即可
  select = Select(driver.find_element_by_id('datemonth'))
  select.select_by_value('3')
  day = driver.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[2]/td[7]/span')#找到日期‘5’，用的是火狐firebug找到的xpath
  day.click()#点击日期


#由于跳转到了登录页面，下面是自动登录
element = driver.find_element_by_name('UserName')
element.send_keys("921202jsy")
element = driver.find_element_by_name('UserPassword')
element.send_keys("921202jay")


driver.close()#关掉当前的标签页，因为总是打不开
driver.switch_to_window(windows[0])#换到第一个标签页
#把刚才的再重新来一遍
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
  select.select_by_value('2014')#作用同上，是另一种方法，二者选一即可
  select = Select(driver.find_element_by_id('datemonth'))
  select.select_by_value('4')
  day = driver.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[2]/td[7]/span')#找到日期‘5’，用的是火狐firebug找到的xpath
  day.click()#点击日期





bisailist = driver.find_elements_by_class_name('op')#找到当天所有的比赛的欧赔列表
len(bisailist)#查看当天比赛数量


#首先是把数据从content中写入MongoDB中的函数，即在具体供公司赔率页面上的操作
def contenttomongodb(content,companyname,urlnum):
  global client
  global db
  sucker1 = '(<a class="bluetxt" href="/soccer/match/)(.*?)(/odds/change/)(.*?)(/">)'
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
    try:
      company = driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')#如果向下滑动鼠标,这个xpath就可能有问题,另外也并不是所有的比赛都有威廉希尔开盘
      company.click()#点开它
    except Exception as e:#有的比赛没有公司开盘，那么就跳出函数
      return
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
      try:
        contenttomongodb(content,companynamelist[i],urlnum)
        print(companynamelist[i]+'_'+urlnum)
      except Exception as e:
        continue
  driver.close()
  driver.switch_to_window(windows[2])#让driver回到单个比赛页面
  driver.close()#把单个比赛页面关闭


#然后是把当天的所有比赛都用danchangbisai函数过一遍，但是这个做不到同时
def dangtianbisai(driver):#此时的driver放在当天的比赛页面上
  initial = driver.current_window_handle
  bisailist = driver.find_elements_by_class_name('op')#找到当天所有的比赛的欧赔列表
  for i in range(0,len(bisailist)):
      try:
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'op')))
      finally:
        bisailist[i].click()#打开当天第一场比赛的欧赔
        windows = driver.window_handles#得到标签页列表
        driver.switch_to_window(windows[2])#把driver转到新打开的那场比赛的标签页上
        danchangbisai(driver)
        driver.switch_to_window(windows[1])


dangtianbisai(driver)
end = time.time()
print(end-start)


#然后就是一个又一个地变换日期,应该建立一个日期池，即从某年某月某日到某年某月某日的一个日期池，日期池中每一个记录包含“年”“月”“日”这三个参数
#将日期池中的记录的三个参数赋予everydaybisai函数，该函数就可以自动抓取当天的比赛数据了。


#首先建立日期池
daypool = list()

def everydaybisai(driver,dateparameter):#此时的driver在“足球日历”的某一天上
  element3 = 
  try:
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,dateparameter的日部分)))
  finally:
    select = Select(driver.find_element_by_id('dateyeah'))#找到选择年份的下拉菜单
    select.select_by_value(dateparameter的年部分)#作用同上，是另一种方法，二者选一即可
    select = Select(driver.find_element_by_id('datemonth'))
    select.select_by_value(dateparameter的月部分)
    day = driver.find_element_by_link_text(dateparameter的日部分)#找到日期‘5’，用的是火狐firebug找到的xpath
    day.click()#点击日期
  bisailist = driver.find_elements_by_class_name('op')#找到当天所有的比赛的欧赔列表
  len(bisailist)#查看当天比赛数量
  dangtianbisai(driver)



  



