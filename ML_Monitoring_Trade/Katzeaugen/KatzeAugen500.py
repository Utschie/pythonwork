#实时监控澳客网赔率，经过测试，500彩票网的赔率更新与betbrains是保持一致的，而澳客网的赔率更新时间数据和500彩票网一样，所以基本上可以认为没有问题
#由于澳客网是动态加载，所以本代码从每场比赛的欧赔加载中找到原始地址,通过请求ajax的原始地址获取数据
#原始地址每个请求返回30个公司赔率数据，这样每场比赛大约6到13个请求，每周大约500到600场比赛，则最多不到8000个请求。
#如果ajax请求的服务器承受能力跟单个公司历史赔率页面相同，那么每秒50个请求来算，同步一周的比赛大约需要3分钟左右的时间
#经试验，请求主页的ajax不需要登陆，但是请求下一周的比赛还是要登录的，所以顺序应该如常，进入主页，登陆，进入日期，获取链接，然后接下来做————20190112
#ajax下来的网页解码方式是unicode-escape，与其他网页不同————20190112
from gevent import monkey;monkey.patch_all()
import os
import re
import gevent
import time
import random#导入随机数模块
from bs4 import BeautifulSoup#在提取代码的时候还是要用到beautifulsoup来提取标签
from datetime import datetime, timedelta, timezone#用来把时间字符串转换成时间
import pytz#用来设置时区信息
import os#用来获取文件名列表
import requests
import urllib
import YDM
import time
import csv
import json#用来将字典写入json文件
import psutil#用来获取内存使用信息以方便释放
import copy #用来复制对象


r = requests.Session()
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
header['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
header['Upgrade-Insecure-Requests'] = '1'#这个也得加上
#经试验，请求主页的ajax不需要登陆，但是请求下一周的比赛还是要登录的，所以顺序应该如常，进入主页，登陆，进入日期，获取链接，然后接下来做
content = a.content.decode('unicode-escape')#注意一旦请求下来后，ajax下来的网页解码方式是这个，与其他网页不同

