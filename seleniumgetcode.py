#虽然可以直接从网上抓代码，但是还是无法动态加载出271个公司的赔率
from selenium import webdriver
import chardet
from bs4 import BeautifulSoup
driver = webdriver.PhantomJS()
driver.get('http://odds.500.com/fenxi1/ouzhi.php?id=519016&ctype=1&start=240&r=1&style=0&guojia=0&chupan=1')#用浏览器打开该网页
ok = driver.page_source.encode()#获取网页源码
chardet.detect(ok)#检验编码方式
ok = ok.decode('utf-8')#解码
ok#显示源码
screenshot = driver.get_screenshot_as_file("D:/screenshot/2.jpg")#注意文件的地址斜杠是正的


