#用来探索澳客网的防盗链原理
import requests
url1 = 'http://www.okooo.com/soccer/match/792591/odds/'
url2 = 'http://www.okooo.com/soccer/match/792591/odds/change/82/'
url3 = 'http://www.okooo.com/soccer/match/?date=2016-03-5'
url4 = 'http://www.okooo.com/soccer/match/'
url5 = 'http://www.okooo.com/soccer/match/792580/odds/'
url6 = 'http://www.okooo.com/soccer/match/792581/odds/'
url7 = 'http://www.okooo.com/soccer/match/983124/odds/'
url8 = 'http://www.okooo.com/soccer/match/799108/odds/'
 
headers = {'Cache-Control':'max-age=0','connection':'keep-alive','referer':'http://www.okooo.com/jingcai/',}
cc = requests.get(url,headers = headers)











GET /soccer/match/792591/odds/ HTTP/1.1
Host: www.okooo.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://www.okooo.com/soccer/match/?date=2016-03-5
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; data_start_isShow=0; PHPSESSID=50bf6e62b9906d50cfba52f4209557d93df38fc8; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1502972534,1502975745,1502977646,1502989714; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1502990246; pm=; LStatus=N; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%u652F%u4ED8%u5B9D%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22qq%22%3A%7B%22LoginCn%22%3A%22QQ%u767B%u5F55%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%u4EBA%u4EBA%u7F51%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%u767E%u5EA6%22%7D%2C%22weixin%22%3A%7B%22LoginCn%22%3A%22%u5FAE%u4FE1%u767B%u5F55%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%u76DB%u5927%u767B%u5F55%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%22%22%2C%22loginSession%22%3A%22___GlobalSession%22%7D; __utma=56961525.1473904416.1501606711.1502972531.1502989711.9; __utmb=56961525.131.6.1502990246394; __utmc=56961525; __utmz=56961525.1501606711.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
If-Modified-Since: Thu, 17 Aug 2017 17:16:32 GMT