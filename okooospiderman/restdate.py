#为了在远程的windows机器上跑的版本
#首先先把文件存储路径改掉，并把相应的三个文件复制到远程机器的D盘data文件夹下
#'/home/jsy/Dropbox/okoookonto_new.csv'澳客网的账户,'file:///home/jsy/Dropbox/useragentswitcher.xml'UA列表
#然后把YDM需要的东西放进路径(未完成)
#把所有的https都改成了http。因为proxies的设置设置为http时在访问http网站时生效，在访问https网站时https生效
#偶尔会在获取验证码的时候卡死，即main2处，应该在此处添加一个重新获取ip登录账户的循环——20181208
#dangtianbisai有时候会进不去，要重播几次才进得去，这里也有循环卡死的风险——20181209
#main函数会出现无法获取验证码循环卡死的情况——20181209
#我怀疑在所有的UA列表中有些UA压根就是不能用的，应该统计一下————20181215
#当出现Error“data does't match format......”的时候，应该不要再重播，以降低ip被ban率。已完成————20181217
#另外，当出现Error"远程主机强制关闭了一个连接或者目标计算机积极拒绝"时应去除这个ip以提高成功爬取率。不行，这样就可能都删光了————20181217
#有时格式不符的公司正是“威廉”，但也不总是。其实应该把格式不符的公司照抓
#代理换成了蜻蜓代理，每次提取10个ip，试一下————20181217
#曾经出现过login超时，应该也给加上次数限制重新提取ip
#通过copy函数和copy库保证ip更换的正确使用。
#通过减小重播间隔，增大重播次数来提高抓取率，甚至提高抓取速度————20181218
#应该把errorlog里的error都打上时间戳，然后用grafana连接errorlog监控爬虫性能————20181219
#改成两场比赛换一次ip看看效率
#应该把更换header的语句也改成用copy的形式————失败了，反而会出现404错误
#由于对面网页改版，程序出现大面积nonetype错误，errorlog大量增加，因此建立一个新的errorlog叫做errorlognew————20190123
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

def checkip(ip):
    global header
    global UAlist
    header4 = header
    iplist = ip
    for i in range(0,len(iplist)):
        error4 = True
        mal3 = 1
        while (error4 ==True and mal3 <= 3):#总共拨三次，首拨1次重拨2次
            try:
                header4['User-Agent'] = random.choice(UAlist)#每尝试一次换一次UA
                check = requests.get('http://www.okooo.com/jingcai/',headers = header4,proxies = {"http":"http://"+ iplist[i]},timeout = 6.5)
            except Exception as e:
                error4 = True
                mal3 = mal3 + 1
                if mal3 > 3:
                    iplist[i] = ''
                    print('第' + str(i) + '个IP不合格，已去除')
            else:
                error4 = False
                print('第' + str(i) + '个IP合格')
    while '' in iplist:
        iplist.remove('')
    return iplist



def dateRange(start, end, step=1, format="%Y-%m-%d"):#生成日期列表函数，用于给datelist赋值
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
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
    with open('D:\\data\\okoookonto_new.csv',"r") as f:#打开文件,并按行读取，每行为一个列表
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
    global proxylist
    header2 = header
    error = True
    while error == True:
        try:
            denglu = r.post('http://www.okooo.com/I/?method=ok.user.login.login',headers = header2,verify=False,data = datas,allow_redirects=False,timeout = 16)#向对面服务器传送数据
            error = False
        except Exception as e:
            print('login超时，正在重拨')
            r.proxies = random.choice(proxylist)#换一个ip
            error = True
    error = True
    while error == True:
        try:
            zuqiuzhongxin = r.get('http://www.okooo.com/soccer/',headers = header2,verify=False,allow_redirects=False,timeout = 16)#进入足球中心
            error = False
        except Exception as e:
            print('login超时，正在重拨')
            r.proxies = random.choice(proxylist)#换一个ip
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
            r.proxies = random.choice(proxylist)#换一个ip
            error = True


def coprocess(urllist,date):#用协程的方式并发打开其他公司，并爬取数据，在dangtianbisai函数里被执行
    ge = list()
    for i in urllist:
        ge.append(gevent.spawn(datatofile,i,date))
    gevent.joinall(ge)


def datatofile(url,date):#在coprocess里被执行,不同公司共用一个ip
    global header
    global r
    global proxylist
    global UAlist
    proxyzanshi = proxylist.copy()#必须用copy这个函数,否则proxylist也会随着proxyzanshi的改变而改变
    proxy = random.choice(proxyzanshi)
    header4 = header
    header4['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header4['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    header4['User-Agent'] = random.choice(UAlist)
    error3 = True
    mal = 1
    while (error3 == True and mal <= 5):#算上1次首拨和3次重拨，总共应该是4次
        try:
            firma = r.get(url,headers = header4,verify=False,allow_redirects=False,timeout = 9.5,proxies=proxy)#进入单个公司赔率的网页
            content3 = firma.content.decode('GB18030')#获得该网页的代码
            firma.close()#关闭连接
            del(firma)#释放内存
            #提取数据用beautifulsoup和re结合的方式比较靠谱
            sucker3 = '<a class="bluetxt" href="/soccer/match/(.*?)/odds/change/(.*?)/".*?>'
            sucker4 = '> <b>(.*?)</b>'
            sucker5 = '/schedule/">(.*?)</a>'
            sucker6 = 'odds/">(.*?) vs (.*?)</a>'
            cid = re.search(sucker3,content3).group(2)
            urlnum = re.search(sucker3,content3).group(1)
            companyname = re.search(sucker4,content3).group(1)
            league = re.search(sucker5,content3).group(1)
            zhudui = re.search(sucker6,content3).group(1)
            kedui = re.search(sucker6,content3).group(2)
            soup = BeautifulSoup(content3,"html5lib")#'html5lib'容错率最高
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
            filepath = 'D:\\data\\okooofile\\'+date+'.txt'
            with open(filepath,'a') as f:
                for i in range(0,len(s2)):#每一次变盘就插入一个记录
                    record = {}
                    record['date'] = date
                    record['urlnum'] = urlnum
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
                    record_str = str(record)
                    f.write(record_str)
            print(url)
            error3 = False
        except Exception as e:
            if re.search('.*?赛前.*?',str(e)):
                print('Error:',e)
                print(url + '出错，跳过并写入Errorlognew文件，格式不符')
                with open('D:\\data\\Errorlognew.txt','a') as f:
                    f.write(url + '出错，跳过并写入Errorlognew文件，格式不符')
                    f.write('\n')
                error3 = False
            elif re.search('.*?NoneType.*?',str(e)) and mal <= 4:
                print('Error:',e)
                print(url + '出错，跳过并写入Errorlognew文件，NoneType')
                with open('D:\\data\\Errorlognew.txt','a') as f:
                    f.write(url + '出错，跳过并写入Errorlognew文件，NoneType')
                    f.write('\n')
                error3 = False
            elif re.search('.*?Read timed out.*?',str(e)) and mal <= 4:
                print('Error:',e)
                print('datatofile超时或出错，2到3秒后进行第'+ str(mal) + '次重拨')
                proxy = random.choice(proxyzanshi)#简单的超时不需要剔除ip
                header4['User-Agent'] = random.choice(UAlist)#出错了才换UA
                mal = mal + 1
                time.sleep(random.uniform(2,3))#随机休息
                error3 = True   
            elif re.search('.*?Max retries exceeded.*?',str(e)) and mal <= 4:
                print('Error:',e)
                print('datatofile超时或出错，2到3秒后进行第'+ str(mal) + '次重拨')
                proxyzanshi.remove(proxy)#去掉刚才出错的ip
                proxy = random.choice(proxyzanshi)#出错了才换ip
                header4['User-Agent'] = random.choice(UAlist)#出错了才换UA
                mal = mal + 1
                time.sleep(random.uniform(2,3))#随机休息
                error3 = True    
            else:
                print(url + '出错，跳过并写入Errorlognew文件，重拨4次')
                with open('D:\\data\\Errorlognew.txt','a') as f:
                    f.write(url + '出错，跳过并写入Errorlognew文件，重拨4次')
                    f.write('\n')
                error3 = False




def dangtianbisai(date,startgame = 0):#在这之前需要先生成一个date列表，由于一天只有一个IP会造成datatofile超时，所以决定每3场比赛重新提取一次IP
    global header
    global r
    global proxylist
    global UAlist
    starttime = time.time()
    header3 = header
    header3['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header3['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    header3['User-Agent'] = random.choice(UAlist)
    error = True
    while error == True:
        try:
            wangye = r.get('http://www.okooo.com/soccer/match/?date=' + date,headers = header3,verify=False,allow_redirects=False,timeout = 31)
            error = False
        except Exception as e:
            print('dangtianbisai超时1，10秒后重拨')
            header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
            r.proxies = random.choice(proxylist)#出错了才换IP
            time.sleep(10)
            error = True
    print('进入日期：'+ date)
    content1 = wangye.content.decode('gb18030')#取出wangye的源代码
    sucker1 = '/soccer/match/.*?/odds/'
    bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
    print('从'+ date +'第'+ str(startgame) + '场比赛开始爬取')
    print(str(bisaiurl))
    for i in range(startgame,len(bisaiurl)):#从断点开始（如果有的话）每场比赛换一个ip爬取,同时也换一个UA
        if (i%2 == 0 and i != 0):#如果是3的倍数且不等于零，则提取一组新ip
            print('已经爬了2场比赛，需要重新提取新ip')
            proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1') #接入混拨（蜻蜓）代理
            print('已获取IP')
            proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
            print('正在检查IP')
            proxylist = checkip(proxylist)
            for j in range(0,len(proxylist)):
                proxylist[j] = {"http":"http://" + proxylist[j],}
            print(proxylist)
            r.proxies = random.choice(proxylist)
            while (len(proxylist) <=4):
                print('有效ip数目不足，需等待10秒重新提取')
                time.sleep(10)
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for j in range(0,len(proxylist)):
                    proxylist[j] = {"http":"http://" + proxylist[j],}
                print(proxylist)
                r.proxies = random.choice(proxylist)
        time.sleep(random.uniform(1,3))#每场比赛爬去之间间隔1到3秒
        error2 = True
        mal2 = 1
        proxyzanshi = proxylist.copy()
        while (error2 == True and mal2 <= 4):#1次首拨，3次重拨，共4次
            try:
                william = r.get('http://www.okooo.com' + bisaiurl[i] + 'change/14/',headers = header3,timeout = 31)#打开威廉希尔
                content2 = william.content.decode('gb18030')
                sucker2 = bisaiurl[i] + 'change/.*?/'
                companyurl = re.findall(sucker2,content2)#从威廉的源码中获取其他公司的链接
                if (len(companyurl) < 3 and mal2 <= 3):
                    print('日期' + date + '第' + str(i) +'场比赛出错,无法从威廉源码中获取其他公司链接,10秒后重拨第'+ str(mal2) +'次')
                    mal2 = mal2 + 1
                    header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
                    proxyzanshi.remove(r.proxies)
                    r.proxies = random.choice(proxyzanshi)#出错了才换ip
                    time.sleep(10)
                    error2 = True
                else:
                    error2 = False
            except Exception as e:
                print('dangtianbisai' + '进入' + bisaiurl[i] + '超时，10秒后重拨第' + str(mal2) +'次')
                mal2 = mal2 + 1
                header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
                proxyzanshi.remove(r.proxies)
                r.proxies = random.choice(proxyzanshi)#出错了才换ip
                time.sleep(10)
                error2 = True
        if (len(companyurl) < 3):
            print('日期' + date + '第' + str(i) +'场比赛出错，无法从威廉源码中获取其他公司链接,跳过并写入Errorlognew文件')
            with open('D:\\data\\Errorlognew.txt','a') as f:
                f.write(bisaiurl[i] + '，日期' + date + '第' + str(i) +'场比赛出错，没有威廉')
                f.write('\n')
            with open('D:\\data\\okooolog.txt','w') as f:
                f.write(date+str(i))#出错跳过的日期也要在日志中记录下爬取进度
            continue
        for j in range(0,len(companyurl)):
            companyurl[j] = 'http://www.okooo.com' + companyurl[j]
        coprocess(companyurl,date)
        print('日期' + date + '第' + str(i) +'场比赛爬取成功')
        with open('D:\\data\\okooolog.txt','w') as f:
            f.write(date+str(i))#在日志中记录下爬取进度
    endtime = time.time()
    print('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endtime - starttime) + '秒' + '\n')
    with open('D:\\data\\finished.txt',"at") as f:
        f.write('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endtime - starttime) + '秒' + '\n')
        f.write('\n')


class Startpoint(object):#定义起始点类，给出日志路径就能得到爬去日期和比赛场次
    def __init__(self,logpath):
        self.logpath = logpath
        log = open(self.logpath,'r')
        try:
            logrecord = log.readline().strip('\n')
            log.close()
            if logrecord != '':
                self.startdate = logrecord[0:10]#前十位是日期
                self.startgame = int(logrecord[10:])#后面是比赛的序号
            else:
                self.startdate = datetime.now().strftime('%Y-%m-%d')
                self.startgame = '0'
        except Exception as e:
            print('Error:',e)
            self.startdate = datetime.now().strftime('%Y-%m-%d')
            self.startgame = '0'


def main():#从打开首页到登录成功
    global header
    global r
    global proxylist
    error = True
    while error == True:
        try:
            r.get('http://www.okooo.com/jingcai/',headers = header,verify=False,allow_redirects=False,timeout = 31)#从首页开启会话
            error = False
        except Exception as e:
            print('Error:',e)
            print('main超时，正在重拨1')
            r.proxies = random.choice(proxylist)
            error = True
    error = True
    mal3 = 0
    while error == True:
        try:
            yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,verify=False,allow_redirects=False,timeout = 31)#get请求登录的验证码
            error = False
        except Exception as e:
            if (mal3%3 != 0 or mal3 == 0):
                mal3 = mal3 + 1
                print('Error:',e)
                print('main超时，正在进行第'+str(mal3)+'次重拨2,')
                r.proxies = random.choice(proxylist)
                error = True
            else:
                print('main获取验证码失败，10秒后重启回话，重新提取ip')
                r.close()
                time.sleep(10)
                header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
                header['User-Agent'] = random.choice(UAlist)
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1') #接入混拨代理
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for j in range(0,len(proxylist)):
                    proxylist[j] = {"http":"http://" + proxylist[j],}
                print(proxylist)
                while (len(proxylist) <=4):
                    print('有效ip数目不足，需等待15秒重新提取')
                    time.sleep(10)
                    proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')
                    print('已获取IP')
                    proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                    print('正在检查IP')
                    proxylist = checkip(proxylist)
                    for j in range(0,len(proxylist)):
                        proxylist[j] = {"http":"http://" + proxylist[j],}
                    print(proxylist)
                r = requests.Session()#开启会话
                r.proxies = random.choice(proxylist)
                error = True           
    filepath = 'D:\\data\\yanzhengma.png'
    with open(filepath,"wb") as f:
        f.write(yanzhengma.content)#保存验证码到本地
    print('已获得验证码')
    datas = randomdatas(filepath)#生成随机账户的datas
    while len(datas['AuthCode']) != 5:#如果验证码识别有问题，那就重新来
        r = requests.Session()#开启会话
        r.proxies = random.choice(proxylist)#使用随机IP
        error = True
        while error == True:
            try:
                r.get('http://www.okooo.com/jingcai/',headers = header,verify=False,allow_redirects=False,timeout = 31)
                error = False
            except Exception as e:
                print('Error:',e)
                print('main超时，正在重拨3')
                r.proxies = random.choice(proxylist)
                error = True
        error = True
        while error == True:
            try:
                yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,verify=False,allow_redirects=False,timeout = 31)#get请求登录的验证码
                error = False
            except Exception as e:
                print('main超时，正在重拨4')
                r.proxies = random.choice(proxylist)
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
UAcontent = urllib.request.urlopen('file:///D:/data/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
logpath = 'D:\\data\\okooolog.txt'
error = True
n = 0
while error == True:
    beginpoint = Startpoint(logpath)#得到起始点信息
    datelist = ['2015-12-25','2018-09-19','2017-03-23','2017-07-04','2018-12-09','2018-09-17','2015-07-14','2018-12-08','2018-12-07','2017-07-05','2018-12-06','2018-07-18','2017-07-06','2018-09-18','2017-07-07','2018-12-05','2018-05-07','2018-12-04','2016-04-29','2018-11-19','2018-09-20']
    datelist.reverse()#让列表倒序，使得爬虫从最近的一天往前爬
    try:
        for i in datelist:#开启一个循环，保证爬取每天的数据用的UA，IP，账户都不一样
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
            header['User-Agent'] = random.choice(UAlist)
            proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1') #接入混拨代理
            print('已获取IP')
            proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
            print('正在检查IP')
            proxylist = checkip(proxylist)
            for j in range(0,len(proxylist)):
                proxylist[j] = {"http":"http://" + proxylist[j],}
            print(proxylist)
            while (len(proxylist) <=4):
                print('有效ip数目不足，需等待15秒重新提取')
                time.sleep(10)
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for j in range(0,len(proxylist)):
                    proxylist[j] = {"http":"http://" + proxylist[j],}
                print(proxylist)
            r = requests.Session()#开启会话
            r.proxies = random.choice(proxylist)
            main()
            ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01',headers = header,verify=False,allow_redirects=False,timeout = 31)#进入1月1日，看看有没有重定向，有的话需要重新登录
            while (ceshi.status_code != 200) and (ceshi.status_code != 203):#'!=200'意味着重定向到了登录页面，登录页面的验证码请求是加密的其他url，无法从此登录
                print(str(ceshi.status_code))
                print('登录失败，正在重新登录')
                time.sleep(10)
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')#接入混拨代理
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for l in range(0,len(proxylist)):
                    proxylist[l] = {"http":"http://"+ proxylist[l],}
                print(proxylist)
                while (len(proxylist) <=4):
                    print('有效ip数目不足，需等待15秒重新提取')
                    time.sleep(10)
                    proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')
                    print('已获取IP')
                    proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                    print('正在检查IP')
                    proxylist = checkip(proxylist)
                    for j in range(0,len(proxylist)):
                        proxylist[j] = {"http":"http://" + proxylist[j],}
                    print(proxylist)
                header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
                header['User-Agent'] = random.choice(UAlist)
                r = requests.Session()#开启会话
                r.proxies = random.choice(proxylist)
                main()
                ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01',headers = header,verify=False,allow_redirects=False,timeout = 31)
            print('登录成功')
            print('准备进入：' + i)
            if n == 0:
                dangtianbisai(i,int(beginpoint.startgame))#从断点比赛开始爬取数据，并在屏幕打印出用时
            else:
                dangtianbisai(i)
            n = 1
            r.close()#关闭会话
            error = False
    except Exception as e:
        print('Error:',e)
        print('IP不可用，需要重新提取')
        time.sleep(15)
        n = 0
        error = True



end = time.time()
print('任务完毕，总用时' + str(end-start) + '秒,任务日期：' + str(datelist[-1]) + '——' + str(datelist[0]))
