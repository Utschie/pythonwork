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

try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')))
finally:
  company = driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[3]/td[6]/a/span')#如果向下滑动鼠标,这个xpath就可能有问题,另外也并不是所有的比赛都有威廉希尔开盘
  company.click()#点开它


windows = driver.window_handles#得到标签页列表
driver.switch_to_window(windows[3])#把driver转到赔率变化的那个标签页上
driver.current_url#查看当前标签页的url

content = driver.page_source#此时的content就是我们想要的那张网页的源码
#接下来就采用函数将提取源码中有效的信息到MongoDB里了

