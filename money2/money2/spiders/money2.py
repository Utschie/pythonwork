#就是那个抓电影名称，排名，评分和评论的spider文件
import scrapy
from money2.items import Money2Item
from scrapy.selector import Selector
class Moneyspider(scrapy.Spider):
    name = "money2"
    allowed_domains = ["www.moviepilot.de"]
    start_urls = ["http://www.moviepilot.de/filme/beste?page=1"]#从第一页开始
    def parse(self,response):
        #在当前页面找到要提取的item并提取出来
        a = response.xpath('//*[@id="archive-content"]/div[2]/ul/li')
        for film in a:
            item = Money2Item()
            #以下的item都是整理好了的，就是格式干干净净可以直接入库的
            item['film_name'] = film.xpath('./div[3]/a[1]/strong').re('<strong itemprop=\"name\">(.*?)</strong>')[0]
            item['film_rank'] = film.xpath('./div[1]').re('<div class=\"ordered-number\">\\n(.*?)\.\\n</div>')[0]
            item['film_mark1'] = film.xpath('./div[3]/div[2]/div[1]/div[1]/div').re('/div>\\n(.*?)\\n<div')[0]
            item['film_mark2'] = film.xpath('./div[3]/div[2]/div[1]/div[2]/div').re('/div>\\n(.*?)\\n<div')[0]
            yield item
        #查找下一页，如果有就点击
        css = '.js--pagination--next'
        next_page = response.css(css)
        if next_page:                 
            url = 'http://www.moviepilot.de'+ next_page[0].re('href=\"(.*?)\"')[0]
            yield scrapy.Request(url,self.parse)
        