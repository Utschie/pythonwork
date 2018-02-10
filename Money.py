#用来赚钱啦
from selenium import webdriver
import requests
import chardet
import re

#首先是爬取电影名称和电影评论，总计大约90000个






#重点是爬取电影评论，由于网站是用脚本加载，因此需要用phantomjs
url = 'http://www.moviepilot.de/movies/'+moviename+'?filter=all'
driver = webdriver.PhantomJS()
driver.get(url)
#打开网页后滚到页面底部，来把评论加载出来
content = driver.page_source
elements = driver.find_element_by_class_name('comment--details collapsible js--collapsible is-initialized')
sucker = '(<p>)(.*?)(</p>)'







 '<div class="comment--details collapsible js--collapsible is-initialized" data-collapsible-classname="comment--collapsible--more" data-collapsible-iconposition="after" style="max-height: none;">
<a class="comment--user" href="/users/zhaoyuan-zhao">
<div class="user--avatar" style="background-image: url(https://assets.cdn.moviepilot.de/files/241c0abdfb13ca876013f554cfb02d5175ffbedb6d4906f8882a574c8c9c/limit/108/80/picture%3Ftype%3Dlarge)"></div>
</a>
<div class="comment--meta">
<a class="comment--username" href="/users/zhaoyuan-zhao">zhaoyuan.zhao</a>
<a class="comment--created-at timeago is-initialized" href="/movies/pulp-fiction/comments/1736795" title="04.09.2017, 00:23" style="visibility: visible;">vor 3 Tagen</a>
<span class="comment--updated-at--label js--updated-at--label" style="display:none">Geändert</span>
<span class="comment--updated-at timeago js--updated-at is-initialized" style="display: none; visibility: visible;" title=""></span>
</div>
<div class="comment--body js--body"><p>Nicht schlecht</p></div>
</div>''




#好像可以用requests直接爬取
url = 'http://www.moviepilot.de/movies/pulp-fiction/comments'+'?page='+str(pagenum)#pagenum是页面总数
code = requests.get('http://www.moviepilot.de/movies/pulp-fiction/comments').content
content = code.decode('utf-8')#content已经把所有的页面都加载出来了
#下面开始提取出评论
sucker = '(<div class=\'comment--body js--body\'>)(.*?)(</div>)'
sucker2 = re.compile(sucker,re.DOTALL)#使sucker2可以匹配换行符
tiqu = sucker2.findall(content)
commentslist = list()
for i in range(0,len(tiqu)):
    commentslist.append(tiqu[i][1])


#这样commentslist就把这一页的评论提取出来了





