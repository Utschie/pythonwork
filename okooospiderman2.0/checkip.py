#用来检测ip池可用情况
import requests
import csv
import re
filename = '/home/jsy/Dropbox/ippool.csv'

def getiplist(filepath):
    iplist = list()
    with open(filepath,"r") as f:
        iplist = f.readlines()
    for i in range(0,len(iplist)):
        iplist[i] = re.search('(.*?)\n',iplist[i]).group(1)
    return iplist

def checkip(ip):
    iplist = ip
    for i in range(0,len(iplist)):
        try:
            requests.get('http://www.okooo.com/jingcai/',headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},proxies = {"http":"http://"+ iplist[i]})
        except Exception as e:
            iplist[i] = ''
        else:
            continue
    while '' in iplist:
        iplist.remove('')
    return iplist

iplist = getiplist(filename)
iplist = checkip(iplist)




'218.81.70.42:37239'
