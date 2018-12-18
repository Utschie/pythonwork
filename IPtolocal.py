#使用独享秒切，每隔20到30秒请求一个ip，共请求6000个，组成本地IP池
import requests
import time
import random
address = '/home/jsy/Dropbox/ippool.csv'
for i in range(0,6000):
    ip = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD201710301636iTCovo/a2abe96f832111e7bcaf7cd30abda612?returnType=1').text
    with open(address,"at") as f:
        f.write(ip)
        f.write('\n')
    time.sleep(random.randint(15,20))


print('over')
