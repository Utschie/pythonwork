#重大突破！重大突破！重大突破！！！
#使用这组代码再也不用先把网页下载到本地再爬取了！！！！！
#就可以在线直接爬取了！！！！
#动态加载的那些url也找到了！！！！！
#多线程多进程协程技术也可能用得上了！！！！
import urllib.request
import chardet
import gzip#加载gzip库，用来解压gzip压缩文件
url = 'http://odds.500.com/fenxi1/ouzhi.php?id=519016&ctype=1&start=30&r=1&style=0&guojia=0&chupan=1'
#print(url)
page = urllib.request.urlopen(url).read()
#print(page)
originalcontent = gzip.decompress(page)#page是由服务器端传来的gzip格式的压缩文件，需要用gzip包来解压缩
#print(originalcontent)
chardet.detect(originalcontent)#检测originalcontent编码
content = originalcontent.decode("utf-8")
#print(content)
sucker12 = '("display:;">)(.*?)(</span>)'
name = re.findall(sucker12,content)
bocaicompany2 = list()
for i in range(0,int(len(name))):
      bocaicompany2.append(name[i][1])  


