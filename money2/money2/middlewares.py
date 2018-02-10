# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
#除了查google以外，使用scrapy shell测试之外以及看scrapy文件夹下的downloadermiddleware
#也能找到有用的东西
#在这个下载器中间件里我添加了ip池和UA池，并把模块儿放到scrapy文件夹里，不过
#好像这个网站被墙了，所以国内的代理ip打不开
from scrapy import signals
from scrapy.tools.IP_UApool import RandomIP, RandomUA

class Money2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomIPMiddleware(object):
    #用来设置随机IP，每次请求都在一个IP池中随机抽取IP
    def process_request(self,request,spider):
        get_ip = RandomIP()
        request.meta['proxy'] = 'http://' + get_ip.get_random_ip()
        print(request.meta['proxy'])


class RandomUAMiddleware(object):
    #用来设置随机UA，每次请求都在一个UA池中随机抽取UA
    def process_request(self,request,spider):
        get_ua = RandomUA()
        request.headers['User-Agent'] = get_ua.get_random_ua()
        print(request.headers['User-Agent'])
