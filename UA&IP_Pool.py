#得到各种UA池
#得到spider的ip地址
import urllib.request
import re
UAcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for i in range(0,int(len(name))):    
    UAlist.append(name[i][1])

UAlist = UAlist[0:586]
#这样就得到了一个拥有586个UA的UA池
