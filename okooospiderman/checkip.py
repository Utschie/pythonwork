#用来检测ip代理商的ip性能
import requests
import urllib
import re
import random
UAcontent = urllib.request.urlopen('file:///D:/data/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
header['User-Agent'] = random.choice(UAlist)
UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
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

proxycontent = requests.get('https://proxy.horocn.com/api/proxies?order_id=TNYW1620117609276472&num=10&format=text&line_separator=win')
print('已获取IP')
proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
print('正在检查IP')
proxylist = checkip(proxylist)
for j in range(0,len(proxylist)):
    proxylist[j] = {"http":"http://" + proxylist[j],}
    print(proxylist)

