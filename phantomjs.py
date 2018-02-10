#selenium自动使用chrome，然后为之后使用PhantomJS做准备
from selenium import webdriver
driver = webdriver.PhantomJS()#打开一个chrome浏览器
driver.get('http://www.okooo.com/jingcai/')#进入这个页面
elemlist = driver.find_elements_by_link_text('欧')#找到所有文字为“欧”的元素组成一个列表
elemlist[0].click()#点击列表中第一个元素
elemlist[1].click()#点击列表中第二个元素
elemlist[2].click()#点击列表中第三个元素
windows = driver.window_handles#得到当前打开的标签页的列表
driver.current_window_handle#查看当前所在的标签页
driver.current_url#查看当前标签页的url
driver.switch_to_window(windows[1])#换到第二个标签页
driver.current_url#再查看一次当前标签页的url

