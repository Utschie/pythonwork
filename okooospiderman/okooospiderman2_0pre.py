#由于登录需要验证码所以，首先用selenium自动登录获取cookie
#这里还可以加一个云打码的API，到时候直接云端识别验证码，就不用人工识别二次粘贴了
from selenium import webdriver
from selenium.webdriver.common.by import By#用来添加显示等待
from selenium.webdriver.support.ui import WebDriverWait#用来添加显示等待
from selenium.webdriver.support import expected_conditions as EC#用来添加显示等待
from selenium.webdriver.common.keys import Keys#用来实现自动登录
from selenium.webdriver.common.action_chains import ActionChains#用来新打开一个标签页
from PIL import Image#用来截图验证码
import requests#用来给爬虫部分挂cookies提供请求
driver = webdriver.Chrome()#打开一个chrome浏览器
driver.get('http://www.okooo.com/jingcai/')#进入这个页面
try:
  element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,'登录')))#等到“登录”这个按钮可以点开
finally:
  element2 = driver.find_element_by_link_text('登录')#找到“登录”按钮
  element2.click()#点开


element = driver.find_element_by_name('login_name')#找到输入用户名的框
element.send_keys("921202jsy")#输入用户名
element = driver.find_element_by_name('login_pwd')#找到输入密码的框
element.send_keys("921202jay")#输入密码
#element = driver.find_element_by_name('randomNoImg')#找到验证码的元素
#imgurl = element.get_attribute('src')#找到验证码元素
#location = element.location#找到验证码位置
#size = element.size#找到验证码大小
#driver.maximize_window()#最大化窗口
#driver.save_screenshot('/home/jsy//screenshot/jietu.png')#必须最大化窗口后再截图，坐标才是对的
#rangle = (int(location['x']),int(location['y']),int(location['x'])+int(size['width']),int(location['y'])+int(size['height']))#给出截图的四个点坐标
#jietu=Image.open('/home/jsy//screenshot/jietu.png') #打开截图
#yanzhengma=jietu.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
#yanzhengma.save('/home/jsy/screenshot/yanzhengma.png')


#人工识别验证码,然后传入验证码
element = driver.find_element_by_name('AuthCode')#找到验证码输入框
element.send_keys("b2nt6")#输入验证码
driver.delete_all_cookies#清除cookies
element = driver.find_element_by_name('Submit')#找到登录按钮
element.click()#点击，登录成功
cookielist = driver.get_cookies()#获得cookielist,需要进一步处理才能被作为cookie重新挂上去

#cookie = {'FirstOKURL':'http%3A//www.okooo.com/jingcai/'; 'First_Source':'www.okooo.com'; 'LastUrl':''; 'Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b':'1508022729,1508087475,1508088763,1508149619'; 'Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b':'1508151519'; '__utma':'56961525.1690251585.1508006783.1508149614.1508151517.5'; '__utmb':'56961525.3.8.1508151518604'; '__utmc':'56961525'; '__utmz':'56961525.1508006783.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)';'PHPSESSID':'3fb3bac4d54b4ebe763e5496ffcc96d716c674a3';'DRUPAL_LOGGED_IN':'Y'; 'IMUserID':'23740465'; 'IMUserName':'921202jsy'; 'OkAutoUuid':'18ebe74c0bc06ed3fafdcd2bfe14697b'; 'OkMsIndex':'6'; 'isInvitePurview':'0';'UWord':'c43b26416f451bec1b0438d301cbf671bb5';}
driver.quit()#得到cookies后就可以关掉了


#接下来就是爬虫部分了，不关闭终端，利用requests库挂上cookies请求网页
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
r = requests.Session()
url = 'http://www.okooo.com/soccer/match/?date=2017-10-7'
s = r.get(url,headers = header,cookies = cookie)
