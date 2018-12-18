#本程序用来清理无效的UA
#经测试全部有效
import urllib
import re
import requests

UAcontent = urllib.request.urlopen('file:///home/jsy/Dropbox/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
print(UAlist)
header = {}
wuxiaoUA = list()
for i in range(0,len(UAlist)):
    header['User-Agent'] = UAlist[i]
    print('正在测试第'+ str(i) +'个UA')
    ceshi = requests.get('http://www.okooo.com/',headers = header,timeout = 16)
    if ceshi.status_code != 200:
        print('无效')
        wuxiaoUA.append(header['User-Agent'])
    else:
        print('有效')


print('UA清理完毕'+ '共' + str(len(wuxiaoUA)) + '个无效UA')
