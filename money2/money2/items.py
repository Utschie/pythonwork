# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 爬取某电影评分网站上的名称，排名，评分以及评论
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Money2Item(scrapy.Item):
    film_name = scrapy.Field()
    film_rank = scrapy.Field()
    film_mark1 = scrapy.Field()
    film_mark2 = scrapy.Field() 
