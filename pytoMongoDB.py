#将数据拿下来的数据写入MongoDB
from pymongo import MongoClient
client = MongoClient()
#用字典创建变量列表，这样就可以批量命名变量了
#创建数据库Library
db = client['lottotxtC']
#创建数据集，相当于关系型数据库里的表
collection = db['bianpanseries']
#创建document，相当于关系型数据库里的行
seriesdict = {}
def pytoMongoDB(urlnum):
  global seriesdict
  global client
  global collection
  seriesdict = {}
  seriesdict['title'] = 
  seriesdict['time'] = 
  seriesdict['win'] = 
  seriesdict['x'] = 
  seriesdict['lose'] = 
  #接下来把document插入数据集
  collection.insert(seriesdict)

  


  


