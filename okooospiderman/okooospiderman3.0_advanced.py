#本爬虫结构：一个用户爬一天，一天之内一个ip爬三场比赛，一场比赛之内所有公司做一个协程。
#最新版本基本上可以用了，唯一的问题是，会莫名其妙的卡住，程序完全停止，也不占用cpu，可能是gevent的问题
#好像可能是遇到了死锁问题
#还是考虑换scrapy吧
#好像问题解决了，并不是gevent的问题，而是超时时间可能设置太短了。现在我把超时后的错误都让他们打印出些能标志他们位置的字来，问题就解决了——2017年10月29日
#把插入数据库的collection名字改了一下，加上了日期，这样断点的时候比较容易找到上次在哪里停止————2017年12月11日
#datatoDB环节有时出现不明原因的“datatoDB超时，正在重拨”一直循环，应设立跳出机制,然后把出问题的网页地址或者日期地址写入到一个日志里，等所有任务完成后再补上这些网页————2017年12月11日
#dangtianbisai有时也出现上述问题
#main也开始出现这样的问题
#datatoDB函数中加了一个随机换UA，结果开始出现个别nonetype报错的情况了，我怀疑是有些UA是无效的，应该写一个checkUA函数,然后把UA列表更新一下
#UA全部有效，还是报错，应该输出为日志————2017年12月11日
#当一天爬取十几场比赛时，就会出现datatoDB超时的情况，并且越来越频繁，应该每10场或者15场比赛提取一组新的ip
#检查ip的时候有时候会出现卡住的情况
#中途换ip居然出现了问题
#即便如此还是会出现datatoDB超时的情况，所以，我决定给设置重拨次数，当重拨超过一定次数后，直接跳过
#另外ip检测通过率低的话，需要等待一段时间重新提取
#其实dangtianbisai,main等函数也应该设置重拨次数限制
#现在在考虑构造一个几百个ip的长效ip池不知道够不够用
#另外，有的时候出现什么都没有就说爬取成功的情况，所以应该是代码有问题，让程序直接绕过其他部分，打印出爬取成功这句话。————2017年12月12日
#上面的问题可能是在从威廉页面提取出其他公司链接的时候出错导致的
#本程序再升级的话就是应该在checkip函数升一下级，首先缩短超时时间，然后应该每个ip尝试3次，三次都不行才被淘汰————2017年12月12日
#其次，错误处理时应该把错误说明一并写到Errorlog里，否则难以知道是什么问题
#不过此处有一个疑惑是，这个程序似乎没有释放内存，导致内存占用随着时间推移越积越多
#今天又出现一个超级大bug，11月29日后面那些天明明威廉页面是有其他公司的，可是偏偏说从威廉中得不到url，即便是英超这种大比赛也出错————2017年12月13日
#而且日期一出错就连着出错
#还有一个问题就是，为什么出错时网址和出错信息会打印两遍——————因为代码中威廉的网址确实出现过两次，一次在下拉列表中，一次在下拉列表的下方，而且两次出现都不是datatoDB的规范格式
#有些比赛是没有威廉的，比如谁11月29日的第六场，只有一条必发指数，此时放入出错是合理的，再比如说11月29日第15场，也是一个道理。
#还有的比赛，比如11月29日第7场比赛，除了威廉，其他的赔率公司都有，这就很讨厌了。
#现在基本上除了内存管理问题bug都改好了，唯一需要调的就可能是datatoDB的timeout，不知道是不是过短
#另外每场比赛的威廉应该会被爬两次，不过不影响大局，如果再细抠可能就是这里了。
#当运行了一天之后，会出现一个错误，叫做OSError: [Errno 24] Too many open files
#另外随着程序的运行，内存占用也越积越多
#想到一个可能的方法是，将程序写成脚本，然后在python中使用linux命令，当内存达到一定程度时，暂停爬虫并停止mongodb服务，或许可以释放内存，不过还没尝试过————2018年2月28日
#另一个可能的方法是，或许pymongo也有disconnect()的函数，或许及时断开与数据库的连接可以释放内存，不过还没尝试过————2018年2月28日

#云打码API用的是官网上YDMHTTP调用示例，已经改名为YDM放到Dropbox里了，以后如果换新系统重新配置环境，需要把Dropbox里的YDM放到python的搜索包的路径里。————2018年3月15日
#新的4.0版本需要增加断点续传的功能————2018年8月9日

from gevent import monkey;monkey.patch_all()
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


def checkip(ip):
    global header
    iplist = ip
    for i in range(0,len(iplist)):
        error4 = True
        mal3 = 1
        while (error4 ==True and mal3 <= 3):#总共拨三次，首拨1次重拨2次
            try:
                check = requests.get('http://www.okooo.com/jingcai/',headers = header,proxies = {"http":"http://"+ iplist[i]},timeout = 6.5)
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
        ge.append(gevent.spawn(datatoDB,i,date))
    gevent.joinall(ge)


def datatoDB(url,date):#在coprocess里被执行,不同公司公用一个ip
    global header
    global client
    global db
    global r
    global proxylist
    global UAlist
    header4 = header
    header4['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header4['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    error3 = True
    mal = 1
    while (error3 == True and mal <= 4):#算上1次首拨和3次重拨，总共应该是4次
        try:
            firma = r.get(url,headers = header4,verify=False,allow_redirects=False,timeout = 9.5)#进入单个公司赔率的网页
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
            collection = db[date + '_'+ urlnum]
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
            print(url)
            error3 = False
        except Exception as e:
            if mal <= 3:
                print('datatoDB超时或出错，10秒后进行第'+ str(mal) + '次重拨')
                r.proxies = random.choice(proxylist)#出错了才换ip
                header4['User-Agent'] = random.choice(UAlist)#出错了才换UA
                mal = mal + 1
                time.sleep(10)
                error3 = True
            else:
                print(url + '出错，跳过并写入Errorlog文件，重拨3次')
                with open('/home/jsy/Dropbox/Errorlog_2.txt','a') as f:
                    f.write(url + '出错，跳过并写入Errorlog文件，重拨3次')
                    f.write('\n')
                error3 = False




def dangtianbisai(date):#在这之前需要先生成一个date列表，由于一天只有一个IP会造成datatoDB超时，所以决定每3场比赛重新提取一次IP
    global header
    global r
    global proxylist
    global UAlist
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
            print('dangtianbisai超时1，10秒后重拨')
            header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
            r.proxies = random.choice(proxylist)#出错了才换IP
            time.sleep(10)
            error = True
    print('进入日期：'+ date)
    content1 = wangye.content.decode('gb18030')#取出wangye的源代码
    sucker1 = '/soccer/match/.*?/odds/'
    bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
    print(str(bisaiurl))
    for i in range(0,len(bisaiurl)):#每场比赛换一个ip爬取,同时也换一个UA
        if (i%3 == 0 and i != 0):#如果是3的倍数且不等于零，则提取一组新ip
            print('已经爬了3场比赛，需要重新提取新ip')
            proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1') #接入混拨代理
            print('已获取IP')
            proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
            print('正在检查IP')
            proxylist = checkip(proxylist)
            for j in range(0,len(proxylist)):
                proxylist[j] = {"http":"http://" + proxylist[j],}
            print(proxylist)
            while (len(proxylist) <=2):
                print('有效ip数目不足，需等待15秒重新提取')
                time.sleep(15)
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=0a4b8956ad274e579822b533d27f79e1&returnType=1&count=1')
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for j in range(0,len(proxylist)):
                    proxylist[j] = {"http":"http://" + proxylist[j],}
                print(proxylist)
        time.sleep(random.uniform(1,3))#每场比赛爬去之间间隔1到3秒
        error2 = True
        mal2 = 1
        while (error2 == True and mal2 <= 4):#1次首拨，3次重拨，共4次
            try:
                william = r.get('http://www.okooo.com' + bisaiurl[i] + 'change/14/',headers = header3,timeout = 31)#打开威廉希尔
                content2 = william.content.decode('gb18030')
                sucker2 = bisaiurl[i] + 'change/.*?/'
                companyurl = re.findall(sucker2,content2)#从威廉的源码中获取其他公司的链接
                if (len(companyurl) < 3 and mal <= 3):
                    print('日期' + date + '第' + str(i) +'场比赛出错,无法从威廉源码中获取其他公司链接,10秒后重拨第'+ str(mal2) +'次')
                    mal2 = mal2 + 1
                    header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
                    r.proxies = random.choice(proxylist)#出错了才换ip
                    time.sleep(10)
                    error2 = True
                else:
                    error2 = False
            except Exception as e:
                print('dangtianbisai' + '进入' + bisaiurl[i] + '超时，10秒后重拨第' + str(mal2) +'次')
                mal2 = mal2 + 1
                header3['User-Agent'] = random.choice(UAlist)#出错了才换UA
                r.proxies = random.choice(proxylist)#出错了才换ip
                time.sleep(10)
                error2 = True
        if (len(companyurl) < 3):
            print('日期' + date + '第' + str(i) +'场比赛出错，无法从威廉源码中获取其他公司链接,跳过并写入Errorlog文件')
            with open('/home/jsy/Dropbox/Errorlog_2.txt','a') as f:
                f.write(bisaiurl[i] + '，日期' + date + '第' + str(i) +'场比赛出错，没有威廉')
                f.write('\n')
            continue
        for j in range(0,len(companyurl)):
            companyurl[j] = 'http://www.okooo.com' + companyurl[j]
        coprocess(companyurl,date)
        print('日期' + date + '第' + str(i) +'场比赛爬取成功')
    endpoint = time.time()
    print('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endpoint - startpoint) + '秒' + '\n')
    with open('/home/jsy/Dropbox/finished.txt',"at") as f:
        f.write('日期：' + date + '，当天比赛爬取成功' + '用时：' + str(endpoint - startpoint) + '秒' + '\n')
        f.write('\n')


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
            print('main超时，正在重拨1')
            r.proxies = random.choice(proxylist)
            error = True
    error = True
    while error == True:
        try:
            yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,verify=False,allow_redirects=False,timeout = 31)#get请求登录的验证码
            error = False
        except Exception as e:
            print('main超时，正在重拨2')
            r.proxies = random.choice(proxylist)
            error = True
    filepath = '/home/jsy/screenshot/yanzhengma.png'
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
datelist = dateRange("2017-09-30", "2017-10-01")#生成一个日期列表
datelist.reverse()#让列表倒序，使得爬虫从最近的一天往前爬
error = True
while error == True:
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
            r = requests.Session()#开启会话
            r.proxies = random.choice(proxylist)
            main()
            ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01',headers = header,verify=False,allow_redirects=False,timeout = 31)#进入1月1日，看看有没有重定向，有的话需要重新登录
            while ceshi.status_code != 200:
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
                header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
                header['User-Agent'] = random.choice(UAlist)
                r = requests.Session()#开启会话
                r.proxies = random.choice(proxylist)
                main()
                ceshi = r.get('http://www.okooo.com/soccer/match/?date=2017-01-01',headers = header,verify=False,allow_redirects=False,timeout = 31)
            print('登录成功')
            print('准备进入：' + i)
            dangtianbisai(i)#爬取当天数据，并在屏幕打印出用时
            r.close()#关闭会话
            error = False
    except Exception as e:
        print('IP不可用，需要重新提取')
        time.sleep(15)
        error = True



end = time.time()
print('任务完毕，总用时' + str(end-start) + '秒,任务日期：' + str(datelist[-1]) + '——' + str(datelist[0]))
