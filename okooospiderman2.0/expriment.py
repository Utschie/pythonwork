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
