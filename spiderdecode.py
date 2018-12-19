#首先把网页保存下来，使之成为本地的一个htm文件
#然后利用python提取该文件的网页代码
#检测编码方式并解码
#如下所示
import urllib.request
import chardet
originalcontent = urllib.request.urlopen('file:///C:/Users/dell/Desktop/expri-page.htm').read()
#originalcontent就是网页的代码
chardet.detect(originalcontent)#检测网页编码
content = originalcontent.decode('gb18030')
#decodecontent就是解码后的网页源码，可以显示中文
content #这就显示出网页代码了
