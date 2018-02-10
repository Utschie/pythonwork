#本程序受武熊博客启发，直接用requests库对澳客网进行模拟登陆，从而无须进行浏览器环境模拟，
#大幅减少CPU占用
import requests
r = requests.Session()#使用session对象是为了保持与服务器的会话，使得一直与服务器保持连接，
#从而cookie等之类的也一直保持着
url = ''
data = {

}
header = {

}
