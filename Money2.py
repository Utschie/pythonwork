#好像不用selenium了
import requests
import re
import chardet
#首先提取电影的名称，排名，和评分
def moviename_rank_grade(pagenum):#pagenum是页面总数
  url = 'http://www.moviepilot.de/filme/beste?page='+str(pagenum)
  code = requests.get(url).content
  content = code.decode('utf-8')


#下面开始提取单个页面的电影名称，排名和评分




#爬取单个页面的电影评论
def moviecomments(pagenum):
  url = 'http://www.moviepilot.de/movies/pulp-fiction/comments'+'?page='+str(pagenum)#pagenum是页面总数
  code = requests.get(url).content
  content = code.decode('utf-8')#content已经把所有的页面都加载出来了
  #下面开始提取出评论
  sucker = '(<div class=\'comment--body js--body\'>)(.*?)(</div>)'
  sucker2 = re.compile(sucker,re.DOTALL)#使sucker2可以匹配换行符
  tiqu = sucker2.findall(content)
  commentslist = list()
  for i in range(0,len(tiqu)):
      commentslist.append(tiqu[i][1])


#下面是协程
