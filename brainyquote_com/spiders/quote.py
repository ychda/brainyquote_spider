# -*- coding: utf-8 -*-
"""
2019-08-02 03:36:38 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 32585004,
 'downloader/request_count': 45340,
 'downloader/request_method_count/GET': 27,
 'downloader/request_method_count/POST': 45313,
 'downloader/response_bytes': 3239594975,
 'downloader/response_count': 45340,
 'downloader/response_status_count/200': 45251,
 'downloader/response_status_count/504': 89,
 'elapsed_time_seconds': 12235.309985,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2019, 8, 1, 19, 36, 38, 159410),
 'httperror/response_ignored_count': 1,
 'httperror/response_ignored_status_count/504': 1,
 'item_scraped_count': 751804,
 'log_count/DEBUG': 797145,
 'log_count/INFO': 214,
 'memusage/max': 125448192,
 'memusage/startup': 55615488,
 'request_depth_max': 30,
 'response_received_count': 45252,
 'retry/count': 88,
 'retry/max_reached': 1,
 'retry/reason_count/504 Gateway Time-out': 88,
 'scheduler/dequeued': 90565,
 'scheduler/dequeued/memory': 90565,
 'scheduler/enqueued': 90565,
 'scheduler/enqueued/memory': 90565,
 'splash/render.html/request_count': 45225,
 'splash/render.html/response_count/200': 45224,
 'splash/render.html/response_count/504': 89,
 'start_time': datetime.datetime(2019, 8, 1, 16, 12, 42, 849425)}
2019-08-02 03:36:38 [scrapy.core.engine] INFO: Spider closed (finished)
"""
import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com/authors']

    """
    从start_urls开始，根据字母排序，页面缺少x字母
    in: https://www.brainyquote.com/authors
    """

    def parse(self, response):
        urls = response.css('h2.indexContentHeader a::attr(href)').getall()
        urls.append('https://www.brainyquote.com/authors/x')
        for url in urls:
            url = response.urljoin(url)
            yield SplashRequest(url, callback=self.parse_author, args={'wait': 0.5})

    """
    根据author主页
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes
    """

    def parse_author(self, response):
        for a in response.css('table.table a'):
            # author = a.xpath('./text()').get()
            url = response.urljoin(a.xpath('.//@href').get())
            yield SplashRequest(url, callback=self.parse_quote, args={'wait': 0.5})
        if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
            page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
            for li in page_ul.xpath('.//li'):
                if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                    next_page = response.urljoin(li.xpath('.//a/@href').get())
                    yield SplashRequest(next_page, callback=self.parse_author, args={'wait': 0.5})

    """
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes的分页页面
    查看html源码，可以看到分页显示有disable属性，但是不影响直接输入url来打开。
    """

    def parse_quote(self, response):
        # for a in response.xpath('//div[@id="quotesList"]//a[@title="view quote"]'):
        for a in response.xpath('//div[@id="quotesList"]//div[@class="qll-bg"]'):
            quote = a.xpath('.//a[@title="view quote"]/text()').get()
            author=a.xpath('.//a[@title="view author"]/text()').get()
            tags = a.xpath('.//div[@class="kw-box"]/a/text()').getall()
            url = a.xpath('.//a[@title="view quote"]//@href').get()
            yield {
                # todo 
                'quote': quote,
                'author': author,
                'tags': tags,
                'url': response.urljoin(url),
            }
        if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
            page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
            for li in page_ul.xpath('.//li'):
                if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                    next_page = response.urljoin(li.xpath('.//a/@href').get())
                    yield SplashRequest(next_page, callback=self.parse_quote, args={'wait': 0.5})
