#用来自动申请澳客网上的账户，把账户名和密码存储在一个txt文件里
#由于申请账户也要验证码，所以还是需要云打码的API
#首先要生成一系列用户名和密码存起来，然后再提交注册
#本程序成功了
#如果循环不是用for而是用while就更好了，这样的话屏幕上输出的个数就可以在出Exception的时候跟实际个数一致
import string
import random
import urllib.request
import re
import requests
import YDM#导入云打码API接口，经一番检查发现可用后就可以使用了
import sys
import time
import hashlib
import csv
# import grequests
from lxml import etree
###############################以下是计算动态转发的接口程序#########################
_version = sys.version_info
is_python3 = (_version[0] == 3)
orderno = "ZF201710233554uJuPWo"
secret = "4811d65dc45949ebb686cc5d08499c90"
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
timestamp = str(int(time.time()))                # 计算时间戳
string1 = ""
string1 = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
if is_python3:
    string1 = string1.encode()

md5_string = hashlib.md5(string1).hexdigest()                 # 计算sign
sign = md5_string.upper()                              # 转换成大写
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
proxy = {"http": "http://" + ip_port}
################################以上是动态转发的接口程序############################
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
    r.proxies = proxy
    header = {'User-Agent': random.choice(UAlist)}#设置UA假装是浏览器
    header['Proxy-Authorization'] = auth
    r.get('http://www.okooo.com/userinfo/register/',headers = header,verify=False,allow_redirects=False)
    yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic&action=register',headers = header,verify=False,allow_redirects=False)
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
    header['Referer'] = 'http://www.okooo.com/userinfo/register/'#必须写上
    header['Upgrade-Insecure-Requests'] = '1'
    register = r.post('http://www.okooo.com/User/SubmitBaseInfo.php',headers = header,data = datas,verify=False,allow_redirects=False)
    with open('/home/jsy/Dropbox/okoookonto.txt',"at") as f:
        f.write(UserName+','+password)
        f.write('\n')

for i in range(0,500):
    try:
        autoregister()
        print('已申请成功第' + str(i+1) + '个账户')
    except Exception as e:
        continue




print('账户申请完毕')





#下面是检验账户是否可用
date = '2017-09-21'
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
header['User-Agent'] = random.choice(UAlist)
header['Proxy-Authorization'] = auth
r = requests.Session()
r.proxies = proxy#使用随机IP
r.verify = False#免证书校验
r.get('http://www.okooo.com/jingcai/',headers = header)
yanzhengma = r.get('http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers = header)#get请求登录的验证码
with open(filepath,"wb") as f:
    f.write(yanzhengma.content)#保存验证码到本地

header3 = header
header3['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
header3['Upgrade-Insecure-Requests'] = '1'#这个也得加上
r.get('http://www.okooo.com/soccer/match/?date=' + date,headers = header3,allow_redirects = 0)

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
datas['AuthCode'] = ydm('/home/jsy/screenshot/yanzhengma.png')#验证码用云打码模块识别
