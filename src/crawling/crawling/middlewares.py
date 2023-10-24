# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import time, datetime
from scrapy.exceptions import IgnoreRequest


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class CrawlingSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CrawlingDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, *args, **kwargs):
        super(ProxyMiddleware, self).__init__(*args, **kwargs)
        self.last_ip_refresh = datetime.datetime.now()
        self.renew_tor_ip()

    def renew_tor_ip(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def renew_ip_if_needed(self, spider):
        spider.logger.warning(f"Changing IP and retrying...")
        now = datetime.datetime.now()
        if (now - self.last_ip_refresh).seconds > 120:  # 120 секунд = 2 минуты
            self.renew_tor_ip()  # ваша функция обновления IP
            self.last_ip_refresh = now
        else: 
            spider.logger.warning(f"Unable to change IP because 2 minutes have not passed")

    def process_response(self, request, response, spider):
        # Get a new identity depending on the response
        spider.logger.info(f"Processing response with status: {response.status} and URL: {response.url}")
        if not (response.status == 200 or (300 <= response.status < 400)) or 'crawlprevention' in response.url:
            self.renew_ip_if_needed(spider=spider)
            request.headers['User-Agent'] = UserAgent().random
            #return request.replace(dont_filter=True)
            # retries = request.meta.get('retry_times', 0) + 1
            
            # if retries <= 3:
            #     spider.logger.warning(f"Attempt #{retries}. Changing IP and retrying...")
            #     for _ in range(3):  # попытайтесь сменить IP до 3 раз
            #         try:
            #             self.renew_tor_ip()
            #             break
            #         except:
            #             time.sleep(3)
            #     request.meta['retry_times'] = retries  # увеличиваем счетчик попыток
            #     return request.replace(dont_filter=True)
            # else:
            #     spider.logger.warning(f"Gave up after {retries} attempts. Skipping URL: {request.url}")
            #     raise IgnoreRequest(f"Failed after {retries} retries")
            
        return response
    
    def process_request(self, request, spider):
        #renew_tor_ip() # uncomment this line if you want to change IP every time
        #request.headers['User-Agent'] = UserAgent().random
        request.meta['proxy'] = 'http://127.0.0.1:8118'

# class RandomUserAgentMiddleware:
#     def __init__(self):
#         self.ua = UserAgent()

#     def process_request(self, request, spider):
#         request.headers['User-Agent'] = self.ua.random
    
#     def process_response(self, request, response, spider):
#         spider.logger.info(f"Processing response with status: {response.status} and URL: {response.url}")
#         if response.status != 200:
#             spider.logger.info("Encountered error, response status code != 200 . Changing IP...")
#             renew_tor_ip()
#             # Повторный запрос к тому же URL после смены IP
#             return request.replace(dont_filter=True)
#         return response
