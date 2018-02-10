# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
import json

class MongoDBPipeline(object):
    collection_name = 'moneydata'
    def __init__(self):
        self.file = open('items.jl','w')#打开一个文件用来保存数据为json格式
        #下面是初始化mongodb的接口
        self.client = pymongo.MongoClient(host = settings['MONGO_HOST'],port = settings['MONGO_PORT']) #指定mongodb端口
        self.db = self.client[settings['MONGO_DB']]#初始化数据库
        self.coll = self.db[settings['MONGO_COLL']]#初始化collection
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+"\n"
        self.file.write(line)#写入文件
        self.coll.insert(dict(item))#得先把item转化成字典形式再插入数据库
        return item
