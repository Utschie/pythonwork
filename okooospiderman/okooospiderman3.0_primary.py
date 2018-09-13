#本版本采用独享代理产品,由于单个ip容易导致datatoDB函数超时效率可能会比advanced版本低一些
#但是省钱
from gevent import monkey;monkey.patch_all()
import requests
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
import time
import csv
def IPapi():
    proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD201710301636iTCovo/a2abe96f832111e7bcaf7cd30abda612?returnType=1')#接入独享代理
    proxy = {"http":"http://"+ proxycontent.text,}
    return proxy

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
    with open('/home/jsy/Dropbox/okoookonto_new.csv',"r") as f:#打开文件,并按行读取，每行为一个列表
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

def login(datas):#把datas给它，它就能进行登录,不切换ip
    global header
    global r
    header2 = header
    error = True
    while error == True:
        try:
            denglu = r.post('http://www.okooo.com/I/?method=user.user.userlogin',headers = header2,verify=False,data = datas,allow_redirects=False,timeout = 16)#向对面服务器传送数据
            error = False
        except Exception as e:
            print('login超时，正在重拨')
            r.proxies = IPapi()#换一个ip
            error = True
    error = True
    while error == True:
        try:
            zuqiuzhongxin = r.get('http://www.okooo.com/soccer/',headers = header2,verify=False,allow_redirects=False,timeout = 16)#进入足球中心
            error = False
        except Exception as e:
            print('login超时，正在重拨')
            r.proxies = IPapi()#换一个ip
            error = True
    header2['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header2['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    error = True
    while error == True:
        try:
            zuqiurili = r.get('http://www.okooo.com/soccer/match/',headers = header2,verify=False,allow_redirects=False,timeout = 16)#进入足球日历,成功
            error = False
        except Exception as e:
            print('login超时，正在重拨')
            r.proxies = IPapi()#换一个ip
            error = True


def coprocess(urllist):#用协程的方式并发打开其他公司，并爬取数据，在dangtianbisai函数里被执行
    ge = list()
    for i in urllist:
        ge.append(gevent.spawn(datatoDB,i))
    gevent.joinall(ge)


def datatoDB(url):#在coprocess里被执行,不同公司公用一个ip
    global header
    global client
    global db
    global r
    header4 = header
    header4['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header4['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    error = True
    while error == True:
        try:
            firma = r.get(url,headers = header4,verify=False,allow_redirects=False,timeout = 30)#进入单个公司赔率的网页
            error = False
        except Exception as e:
            print('datatoDB超时，正在重拨')
            error = True
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
    soup = BeautifulSoup(content3,"html5lib")
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
    print(url)

def dangtianbisai(date):#在这之前需要先生成一个date列表，一天只用一个ip
    global header
    global r
    startpoint = time.time()
    header3 = header
    header3['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header3['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    error = True
    while error == True:
        try:
            wangye = r.get('http://www.okooo.com/soccer/match/?date=' + date,headers = header3,verify=False,allow_redirects=False,timeout = 31)
            error = False
        except Exception as e:
            print('dangtianbisai超时，正在重拨')
            error = True
    print('进入日期：'+ date)
    content1 = wangye.content.decode('gb18030')#取出wangye的源代码
    sucker1 = '/soccer/match/.*?/odds/'
    bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
    print(str(bisaiurl))
    for i in range(0,len(bisaiurl)):#每场比赛换一个ip爬取
        time.sleep(random.uniform(1,3))#每场比赛爬去之间间隔1到3秒
        error = True
        while error == True:
            try:
                william = r.get('http://www.okooo.com' + bisaiurl[i] + 'change/14/',headers = header3,verify=False,allow_redirects=False,timeout = 31)#打开威廉希尔
                error = False
            except Exception as e:
                print('dangtianbisai超时，正在重拨')
                error = True
        content2 = william.content.decode('gb18030')
        sucker2 = bisaiurl[i] + 'change/.*?/'
        companyurl = re.findall(sucker2,content2)#从威廉的源码中获取其他公司的链接
        for j in range(0,len(companyurl)):
            companyurl[j] = 'http://www.okooo.com' + companyurl[j]
        coprocess(companyurl)
        print('日期' + date + '第' + str(i) +'场比赛爬取成功')
    endpoint = time.time()
    print('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endpoint - startpoint) + '秒' + '\n')
    with open('/home/jsy/Dropbox/finished.txt',"at") as f:
        f.write('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endpoint - startpoint) + '秒' + '\n')
        f.write('\n')


def main():
    global header
    global r
    error = True
    while error == True:
        try:
            r.get('http://www.okooo.com/jingcai/',headers = header,verify=False,allow_redirects=False,timeout = 16)
            error = False
        except Exception as e:
            print('main超时，正在重拨')
            error = True
    error = True
    while error == True:
        try:
            yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,verify=False,allow_redirects=False,timeout = 16)#get请求登录的验证码
            error = False
        except Exception as e:
            print('main超时，正在重拨')
            error = True
    filepath = '/home/jsy/screenshot/yanzhengma.png'
    with open(filepath,"wb") as f:
        f.write(yanzhengma.content)#保存验证码到本地
    print('已获得验证码')
    datas = randomdatas(filepath)#生成随机账户的datas
    while len(datas['AuthCode']) != 5:#如果验证码识别有问题，那就重新来
        r = requests.Session()#开启会话
        r.proxies = IPapi()#使用随机IP
        error = True
        while error == True:
            try:
                r.get('http://www.okooo.com/jingcai/',headers = header,verify=False,allow_redirects=False,timeout = 16)
                error = False
            except Exception as e:
                print('main超时，正在重拨')
                error = True
        error = True
        while error == True:
            try:
                yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,verify=False,allow_redirects=False,timeout = 16)#get请求登录的验证码
                error = False
            except Exception as e:
                print('main超时，正在重拨')
                error = True
        with open(filepath,"wb") as f:
            f.write(yanzhengma.content)#保存验证码到本地
        print('已重新获得验证码')
        datas = randomdatas(filepath)#生成随机账户的datas
        print('云打码已尝试一次')
    login(datas)#登录账户
    print('正在登录下面账户:')
    print(str(datas))

####################################以上是函数定义部分##########################################
####################################以下是主程序部分###########################################


start = time.time()
client = MongoClient()
db = client.okooo
UAcontent = urllib.request.urlopen('file:///home/jsy/Dropbox/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
datelist = dateRange("2017-01-01", "2017-10-18")#生成一个日期列表
datelist.reverse()#让列表倒序，使得爬虫从最近的一天往前爬
for i in datelist:#开启一个循环，保证爬取每天的数据用的UA，IP，账户都不一样
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
    header['User-Agent'] = random.choice(UAlist)
    r = requests.Session()#开启会话
    r.proxies = IPapi()
    main()
    ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01' ,headers = header,verify=False,allow_redirects=False,timeout = 31)#进入1月1日，看看有没有重定向，有的话需要重新登录
    while ceshi.status_code != 200:
        print('登录失败，正在重新登录')
        time.sleep(15)
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
        header['User-Agent'] = random.choice(UAlist)
        r = requests.Session()#开启会话
        r.proxies = IPapi()
        main()
        ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01',headers = header,verify=False,allow_redirects=False,timeout = 31)
    print('登录成功')
    print('准备进入：' + i)
    dangtianbisai(i)#爬取当天数据，并在屏幕打印出用时
    r.close()#关闭会话




print('任务完毕')
