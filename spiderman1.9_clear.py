import urllib.request
import chardet
import re
from bs4 import BeautifulSoup
import time
start = time.time()
def pagetotxt(url):
  originalcontent = urllib.request.urlopen(url).read()
  content = originalcontent.decode('gb18030')
  content 
  date = re.search('(<p class="game_time">比赛时间)(.*?)(</p>)',content).group(2)
  date = date[0:10]
  rawtitle = re.search('(<title>)(.*?)(-百家欧赔-500彩票网</title>)',content)
  title = rawtitle.group(2)
  title = re.sub('/','',title)
  title = re.sub('\d','',title)
  saishi = re.search('(\()(.*?)(\))',title).group(2)
  soup = BeautifulSoup(content,"lxml")
  company = soup.find_all(class_ = "tb_plgs")
  company = str(company)
  sucker1 = '("display:;">)(.*?)(</span)'
  rawresult = re.findall(sucker1,company)
  rawresult
  finalresult = list()
  for i in range(0,len(rawresult)):
      finalresult.append(rawresult[i][1])
  bocaicompany = str(finalresult)
  bifen = re.search('(<strong>)(.*?)(</strong>)',content).group(2)
  sucker2 = '("cursor:pointer" >)(.*?)(</td>)'
  number = re.findall(sucker2,content)
  number[3][1]
  peilv = list()
  for i in range(0,int(len(number))):
      peilv.append(number[i][1])  
  sucker2 = '(<td row="1".*? >)(.*?%)(</td>)'
  number = re.findall(sucker2,content)
  jishigailv = list()
  for i in range(0,int(len(number))):
      jishigailv.append(number[i][1])  
  sucker3 = '(<td row="1">)(.*?%)(</td>)'
  number = re.findall(sucker3,content)
  fanhuanlv = list()
  for i in range(0,int(len(number))):
      fanhuanlv.append(number[i][1])  
  sucker4 = '(<td row="1" class="".*?>)(.*?)(</td>)'
  number = re.findall(sucker4,content)
  jishikailiindex = list()
  for i in range(0,int(len(number))):
      jishikailiindex.append(number[i][1])  
  peilv = str(peilv)
  jishigailv = str(jishigailv)
  fanhuanlv = str(fanhuanlv)
  jishikailiindex = str(jishikailiindex)
  address = 'D:\\pythonlabor2\\{date_title}.txt'
  address = address.format(date_title = date+'_'+title)
  with open(address,"w") as f:
    f.write(bocaicompany)
    f.write('\n')
    f.write('\n')
    f.write(date)
    f.write('\n')
    f.write('\n')
    f.write(title)
    f.write('\n')
    f.write('\n')
    f.write(saishi)
    f.write('\n')
    f.write('\n')
    f.write(bifen)
    f.write('\n')
    f.write('\n')
    f.write(peilv)
    f.write('\n')
    f.write('\n')
    f.write(jishigailv)
    f.write('\n')
    f.write('\n')
    f.write(fanhuanlv)
    f.write('\n')
    f.write('\n')
    f.write(jishikailiindex)
    f.write('\n')
    f.write('\n')


for i in range(250000,334549):
    url = 'file:///D:/lottowebpage/odds.500.com/fenxi/ouzhi-{n}.shtml'
    url = url.format(n=i)
    try:
      pagetotxt(url)
      print(i)
    except Exception as e:
      continue


end = time.time()
print('MISSION COMPLETED. I AM THE SPIDERMAN')
print(str(end-start))
