#直接用requests模拟请求，登录，爬取等。已完成
#中间要加个云打码的API，这样就不用人工识别二次粘贴了。已完成
#随机IP池和随机UA池还没有写。已完成
#由于要随机换不同的用户，因此登录也需要写一个函数，即randomdatas函数，用来随机登录。已完成
#这里还需要写一个东西，就是如果验证码识别错误怎么办。
#还有一个，就是如果IP地址不可用怎么办。
#本程序已完成——2017年10月24日0点55，准备明天第一次测试
#经测试在这个网站动态转发不可用——2017年10月27日

import requests
from gevent import monkey; monkey.patch_all()
import re
import gevent
import time
import random#导入随机数模块
from pymongo import MongoClient
from bs4 import BeautifulSoup#在提取代码的时候还是要用到beautifulsoup来提取标签
from datetime import datetime, timedelta, timezone#用来把时间字符串转换成时间
import pytz#用来设置时区信息
import os#用来获取文件名列表
import requests
import urllib
import YDM
import sys
import time
import hashlib
from lxml import etree
import csv
###############################以下是计算动态转发的接口程序#########################
_version = sys.version_info
is_python3 = (_version[0] == 3)
orderno = "ZF201710233554uJuPWo"#订单号
secret = "4811d65dc45949ebb686cc5d08499c90"#我账户上面的secret
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
timestamp = str(int(time.time()))#计算时间戳
string1 = ""
string1 = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
if is_python3:
    string1 = string1.encode()

md5_string = hashlib.md5(string1).hexdigest()#计算sign
sign = md5_string.upper()#转换成大写
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
proxy = {"http": "http://" + ip_port}
################################以上是动态转发的接口程序############################

def dateRange(start, end, step=1, format="%Y-%m-%d"):#生成日期列表函数，用于给datelist赋值
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + timedelta(i), format) for i in range(0, days, step)]

def ydm(filename):#把filepath传给它，他就能得到验证码的验证结果
    username = '921202jsy'
    password  = '921202jay'
    appid = 1
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    yundama = YDM.YDMHttp(username,password,appid,appkey)
    cid, result = yundama.decode(filename, 1005, 60)
    return result

def randomdatas(filename):#把filepath传给它，它就能得到一个随机的登录账户
    User = list()
    with open('/home/jsy/Dropbox/okoookonto.csv',"r") as f:#打开文件,并按行读取，每行为一个列表
         reader = csv.reader(f)
         for row in reader:
             User.append(row)
    datas = {
    'UserName':'',
    'PassWord':'',
    'LoginType':'okooo',
    'RememberMe':'1',
    'AuthType':'okooo',
    'AuthCode':'',
    }#datas的值取决于yundama
    suiji = random.randint(0,len(User)-1)
    datas['UserName'] = User[suiji][0]
    datas['PassWord'] = User[suiji][1]
    datas['AuthCode'] = ydm(filename)#验证码用云打码模块识别
    return datas

def login(datas):#把datas给它，它就能进行登录
    global header
    global r
    header2 = header
    denglu = r.post('http://www.okooo.com/I/?method=user.user.userlogin',headers = header2,data = datas,)#向对面服务器传送数据
    zuqiuzhongxin = r.get('http://www.okooo.com/soccer/',headers = header2,)#进入足球中心
    header2['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header2['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    zuqiurili = r.get('http://www.okooo.com/soccer/match/',headers = header2,)#进入足球日历,成功

def coprocess(urllist):#用协程的方式并发打开其他公司，并爬取数据，在dangtianbisai函数里被执行
  ge = list()
  for i in urllist:
    ge.append(gevent.spawn(datatoDB,i))
  gevent.joinall(ge)
  print()

def datatoDB(url):#在coprocess里被执行
    global header
    global client
    global db
    global r
    header4 = header
    header4['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header4['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    firma = r.get(url,headers = header4)#进入单个公司赔率的网页
    content3 = firma.content.decode('GB18030')#获得该网页的代码
    #提取数据用beautifulsoup和re结合的方式比较靠谱
    sucker3 = '<a class="bluetxt" href="/soccer/match/(.*?)/odds/change/(.*?)/">'
    sucker4 = '> <b>(.*?)</b>'
    sucker5 = '/schedule/">(.*?)</a>'
    sucker6 = 'odds/">(.*?) vs (.*?)</a>'
    cid = re.search(sucker3,content3).group(2)
    urlnum = re.search(sucker3,content3).group(1)
    companyname = re.search(sucker4,content3).group(1)
    league = re.search(sucker5,content3).group(1)
    zhudui = re.search(sucker6,content3).group(1)
    kedui = re.search(sucker6,content3).group(2)
    collection = db[urlnum]
    soup = BeautifulSoup(content3,"lxml")
    table = soup.table
    tr = table.find_all('tr')
    del tr[0],tr[0],tr[1]
    s1 = list()
    for x in range(0,len(tr)):
        s1.append(str(tr[x]))
    sucker7 = '(>)(.*?)(<)'
    s2 = list()#s2为存储时间和赔率的列表
    for u in range(0,len(s1)):
        uu = re.findall(sucker7,s1[u])
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
    tzinfo = pytz.timezone('Etc/GMT-8')#先定义时区信息,这里代表北京时间
    for i in range(0,len(s2)):#把s2中的时间转换成UTC时间
        s2[i][0] = datetime.strptime(s2[i][0][:16],'%Y/%m/%d %H:%M')#先转成datetime实例（北京时间）
        s2[i][0] = s2[i][0].replace(tzinfo = tzinfo)#讲时间都标上北京时间
        s2[i][0] = s2[i][0].astimezone(timezone(timedelta(hours=0)))#转换成utc时间
    for i in range(0,len(s2)):#把概率转化成百分比
        s2[i][5] = round(s2[i][5]*0.01,4)#还必须得四舍五入，要不然不是两位小数
        s2[i][6] = round(s2[i][6]*0.01,4)
        s2[i][7] = round(s2[i][7]*0.01,4)
    for i in range(0,len(s2)):#把剩余时间转化成分钟数
        match = re.match('赛前(.*?)小时(.*?)分',s2[i][1])
        s2[i][1] = int(match.group(1))*60 + int(match.group(2))#转化成据比赛开始前的剩余分钟数
    for i in range(0,len(s2)):#每一次变盘就插入一个记录
        record = {}
        record['league'] = league
        record['cid'] = cid
        record['zhudui'] = zhudui
        record['kedui'] = kedui
        record['companyname'] = companyname
        record['timestamp'] = s2[i][0]
        record['resttime'] = s2[i][1]
        record['peilv'] = [s2[i][2],s2[i][3],s2[i][4]]
        record['gailv'] = [s2[i][5],s2[i][6],s2[i][7]]
        record['kailizhishu'] = [s2[i][8],s2[i][9],s2[i][10]]
        record['fanhuanlv'] = s2[i][11]
        collection.insert(record)

def dangtianbisai(date):#在这之前需要先生成一个date列表，
    global header
    global r
    startpoint = time.time()
    header3 = header
    header3['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header3['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    wangye = r.get('http://www.okooo.com/soccer/match/?date=' + date,headers = header3,)#进入指定日期，成功
    print('进入日期：'+ date)
    content1 = wangye.content.decode('gb18030')#取出wangye的源代码
    sucker1 = '/soccer/match/.*?/odds/'
    bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
    for i in range(0,len(bisaiurl)):#逐个对每个比赛进行爬取
        william = r.get('http://www.okooo.com' + bisaiurl[i] + 'change/14/',headers = header3,)#打开威廉希尔
        content2 = william.content.decode('gb18030')
        sucker2 = bisaiurl[i] + 'change/.*?/'
        companyurl = re.findall(sucker2,content2)#从威廉的源码中获取其他公司的链接
        for j in range(0,len(companyurl)):
            companyurl[j] = 'http://www.okooo.com' + companyurl[j]
        coprocess(companyurl)
    endpoint = time.time()
    print('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endpoint - startpoint) + '秒' + '\n')

####################################以上是函数定义部分##########################################
####################################以下是主程序部分###########################################


start = time.time()
client = MongoClient()
db = client.okooo
UAcontent = urllib.request.urlopen('file:///home/jsy/Dropbox/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for i in range(0,int(len(UAname))):
    UAlist.append(UAname[i][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
datelist = dateRange("2017-01-01", "2017-10-21")#生成一个日期列表
datelist.reverse()#让列表倒序，使得爬虫从最近的一天往前爬
for i in datelist:#开启一个循环，保证爬取每天的数据用的UA，IP，账户都不一样
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
    header['User-Agent'] = random.choice(UAlist)
    header['Proxy-Authorization'] = auth
    r = requests.Session()#开启会话
    r.proxies = proxy#使用随机IP
    r.verify = False#免证书校验
    r.get('http://www.okooo.com/jingcai/',headers = header)
    yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header)#get请求登录的验证码
    print('已获得验证码')
    filepath = '/home/jsy/screenshot/yanzhengma.png'
    with open(filepath,"wb") as f:
        f.write(yanzhengma.content)#保存验证码到本地
    datas = randomdatas(filepath)#生成随机账户的datas
    login(datas)#登录账户
    print('已登录下面账户:')
    print(str(datas))
    dangtianbisai(i)#爬取当天数据，并在屏幕打印出用时
    r.close()#关闭会话
        #with open('/home/jsy/Dropbox/errordate',"at") as v:
        #v.write(i)
        #    v.write('\n')



print('任务完毕')
