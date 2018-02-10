#直接用requests模拟请求，登录，爬取等
#中间可以再加个云打码的API，这样就不用人工识别二次粘贴了
import requests
from gevent import monkey; monkey.patch_all()
import re
import gevent
import time
import random#导入随机数模块
from pymongo import MongoClient
from bs4 import BeautifulSoup#在提取代码的时候还是要用到beautifulsoup来提取标签
import os#用来获取文件名列表
import requests
import urllib
start = time.time()
client = MongoClient()
db = client.okooo
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器

def datatoDB(url):
    global header
    global client
    global db
    company = r.get(url,headers = header)


r = requests.Session()#开启会话
r.get('http://www.okooo.com/jingcai/',headers = header)
yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header)#get请求验证码
with open('/home/jsy/screenshot/yanzhengma.png',"wb") as f:
    f.write(yanzhengma.content)#保存验证码到本地


##########################然后将保存好的验证码传到云打码，将返回的值放到datas里##################






datas = {
'UserName':'shenyigang',
'PassWord':'jinyulao',
'LoginType':'okooo',
'RememberMe':'1',
'AuthType':'okooo',
'AuthCode':'qqezu',
}
denglu = r.post('http://www.okooo.com/I/?method=user.user.userlogin',headers = header,data = datas)#向对面服务器传送数据
zuqiuzhongxin = r.get('http://www.okooo.com/soccer/',headers = header,)#进入足球中心
header['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
header['Upgrade-Insecure-Requests'] = '1'#这个也得加上
zuqiurili = r.get('http://www.okooo.com/soccer/match/',headers = header,)#进入足球日历,成功

wangye = r.get('http://www.okooo.com/soccer/match/?date=2017-10-14',headers = header,)#进入指定日期，成功
content1 = wangye.content.decode('GB2312')#取出wangye的源代码
sucker1 = '/soccer/match/.*?/odds/'
bisaiurl = re.findall(sucker1,content1)
for i in range(0,len(bisaiurl)):
    bisaiurl[i] = 'http://www.okooo.com' + bisaiurl[i]#获得当天所有比赛的链接列表


#bisai = r.get('http://www.okooo.com/soccer/match/984034/odds/',headers = header)#打开单场比赛
william = r.get(bisaiurl[0] + 'change/14/',headers = header)#打开竞彩官方
content2 = william.content.decode('GB2312')
sucker2 = '/soccer/match/.*?/odds/change/.*?/'
companyurl = re.findall(sucker2,content2)
for i in range(0,len(companyurl)):
    companyurl[i] = 'http://www.okooo.com' + companyurl[i]#从william的源码中获取其他公司的链接


def coprocess(urllist):#用协程的方式并发打开其他公司，并爬取数据
  ge = list()
  for i in urllist:
    ge.append(gevent.spawn(datatoDB,i))
  gevent.joinall(ge)
  print()



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
#collection = db[urlnum]
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
    #把s2中的时间转换成UTC时间



###############################自动申请账号程序##########################################################

import string
import random
import urllib.request
import re
import requests
import YDM#导入云打码API接口，经一番检查发现可用后就可以使用了
UAcontent = urllib.request.urlopen('file:///media/jsy/work/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for i in range(0,int(len(UAname))):
    UAlist.append(UAname[i][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
def ydm(filename):
    username = '921202jsy'
    password  = '921202jay'
    appid = 1
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    yundama = YDM.YDMHttp(username,password,appid,appkey)
    cid, result = yundama.decode(filename, 1005, 60)
    return result





def UserName_generator(chars=string.ascii_uppercase +string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for i in range(random.randint(9,16)))


def PassWord_generator(chars=string.ascii_uppercase +string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for i in range(random.randint(8,20)))


def autoregister():
    r = requests.Session()
    header = {'User-Agent': random.choice(UAlist)}#设置UA假装是浏览器
    r.get('http://www.okooo.com/userinfo/register/',headers = header)
    yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic&action=register',headers = header)
    filename = '/home/jsy/screenshot/yanzhengma.png'
    with open(filename,"wb") as f:
        f.write(yanzhengma.content)#保存验证码到本地
    UserName = UserName_generator()
    password = PassWord_generator()
    AuthType =  ydm(filename)
    datas = {
    'username':'dorothy1135',
    'Submit':'1',
    'UserName':UserName,
    'password':password,
    'CPPassword':password,
    'AuthCode':AuthType,
    'AuthType':'okooo',
    'checkRead':'1',
    'UrlFrom':'/member/recomm/',
    }#接下来把验证码图片传到云打码
    header['Origin'] = 'http://www.okooo.com'
    header['Referer'] = 'http://www.okooo.com/userinfo/register/'
    header['Upgrade-Insecure-Requests'] = '1'
    register = r.post('http://www.okooo.com/User/SubmitBaseInfo.php',headers = header,data = datas)
    with open('/home/jsy/Dropbox/okoookonto.txt',"at") as f:
        f.write(UserName+','+password)
        f.write('\n')









r = requests.Session()
header = {'User-Agent': random.choice(UAlist)}#设置UA假装是浏览器
r.get('http://www.okooo.com/userinfo/register/',headers = header)
yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic&action=register',headers = header)
filename = '/home/jsy/screenshot/yanzhengma.png'
with open(filename,"wb") as f:
    f.write(yanzhengma.content)#保存验证码到本地

UserName = UserName_generator()
password = PassWord_generator()
AuthType =  ydm(filename)
datas = {
'username':'dorothy1135',
'Submit':'1',
'UserName':UserName,
'password':password,
'CPPassword':password,
'AuthCode':AuthType,
'AuthType':'okooo',
'checkRead':'1',
'UrlFrom':'/member/recomm/',
}#接下来把验证码图片传到云打码
header['Origin'] = 'http://www.okooo.com'
header['Referer'] = 'http://www.okooo.com/userinfo/register/'
header['Upgrade-Insecure-Requests'] = '1'
register = r.post('http://www.okooo.com/User/SubmitBaseInfo.php',headers = header,data = datas)
with open('/home/jsy/Dropbox/okoookonto.txt',"at") as f:
    f.write(UserName+','+password)
    f.write('\n')


###################################################################################################


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


def ydm(filename):#把filepath传给它，他就能得到验证码的验证结果
    username = '921202jsy'
    password  = '921202jay'
    appid = 1
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    yundama = YDM.YDMHttp(username,password,appid,appkey)
    cid, result = yundama.decode(filename, 1005, 60)
    return result

def login(datas):#把datas给它，它就能进行登录
    global header
    global r
    header2 = header
    denglu = r.post('http://www.okooo.com/I/?method=user.user.userlogin',headers = header2,data = datas,)#向对面服务器传送数据
    zuqiuzhongxin = r.get('http://www.okooo.com/soccer/',headers = header2,)#进入足球中心
    header2['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
    header2['Upgrade-Insecure-Requests'] = '1'#这个也得加上
    zuqiurili = r.get('http://www.okooo.com/soccer/match/',headers = header2,)#进入足球日历,成功

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

for suiji in User:
    try:
        datas['UserName'] = suiji[0]
        datas['PassWord'] = suiji[1]
        date= '2017-09-21'
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
        header['Proxy-Authorization'] = auth
        r = requests.Session()#开启会话
        r.proxies = proxy#使用随机IP
        r.verify = False#免证书校验
        r.get('http://www.okooo.com/jingcai/',headers = header,timeout = 31)
        yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,timeout = 31)#get请求登录的验证码
        filepath = '/home/jsy/screenshot/yanzhengma.png'
        with open(filepath,"wb") as f:
            f.write(yanzhengma.content)#保存验证码到本地
        print('已获得验证码')
        datas['AuthCode'] = ydm(filepath)#验证码用云打码模块识别
        while len(datas['AuthCode']) != 5:
            r = requests.Session()#开启会话
            r.proxies = proxy#使用随机IP
            r.verify = False#免证书校验
            r.get('http://www.okooo.com/jingcai/',headers = header,timeout = 31)
            yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header,timeout = 31)#get请求登录的验证码
            with open(filepath,"wb") as f:
                f.write(yanzhengma.content)#保存验证码到本地
            print('已重新获得验证码')
            datas['AuthCode'] = ydm(filepath)#验证码用云打码模块识别
            print('云打码已尝试一次')
        login(datas)#登录账户
        print('已登录下面账户:')
        print(str(datas))
        header3 = header
        header3['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
        header3['Upgrade-Insecure-Requests'] = '1'#这个也得加上
        wangye = r.get('http://www.okooo.com/soccer/match/?date=' + date,headers = header3,verify=False,allow_redirects=False,timeout = 31)#进入指定日期,并设定超时
        if wangye.status_code == 302 or wangye.status_code == 301:
            with open('/home/jsy/Dropbox/okoookonto_wuxiao.txt',"at") as f:
                f.write(datas['UserName'] + ',' + datas['PassWord'])
                f.write('\n')
            print('无效')
        else:
            with open('/home/jsy/Dropbox/okoookonto_new.txt',"at") as f:
                f.write(datas['UserName'] + ',' + datas['PassWord'])
                f.write('\n')
            print('有效')
    except Exception as e:
        continue









########################################################对checkip函数的改进，每个ip拨号次数变为三次，超时缩短###################################################################
def checkip(ip):
    global header
    iplist = ip
    for i in range(0,len(iplist)):
        error4 = True
        mal3 = 1
        while (error4 ==True and mal3 <= 3):
            try:
                check = requests.get('http://www.okooo.com/jingcai/',headers = header,proxies = {"http":"http://"+ iplist[i]},timeout = 16)
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
############################################################原版checkip函数###################################################3#######################
def checkip(ip):
    global header
    iplist = ip
    for i in range(0,len(iplist)):
        try:
            check = requests.get('http://www.okooo.com/jingcai/',headers = header,proxies = {"http":"http://"+ iplist[i]},timeout = 16)
        except Exception as e:
            print('第' + str(i) + '个IP不合格，已去除')
            iplist[i] = ''
        else:
            print('第' + str(i) + '个IP合格')
            continue
    while '' in iplist:
        iplist.remove('')
    return iplist
