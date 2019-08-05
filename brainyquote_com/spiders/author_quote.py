# -*- coding: utf-8 -*-
"""
    Author: ychda
    Email: ychda@qq.com
    http://www.ychda.cn
    #
    $ scrapy crawl author_quote -a author="lu xun"
    $ scrapy crawl author_quote
    如果不指定参数则在列表中随机选择一个。
"""
import scrapy
import random


class AuthorQuoteSpider(scrapy.Spider):

    def __init__(self, author=None, *args, **kwargs):
        super(AuthorQuoteSpider, self).__init__(*args, **kwargs)
        if author is None:
            author = random.choice(['jack ma', 'lu xun', 'lao tzu', 'sun tzu', 'mencius', 'zhuangzi', 'jenova chen',
                                    'mao zedong', 'mark twain', 'confucius', 'kong zi', 'xun kuang', 'zhou xun', ])
        self.start_urls = ['https://www.brainyquote.com/search_results?q=' + ('+'.join(author.split(' ')))]

    name = 'author_quote'

    allowed_domains = ['brainyquote.com']

    """
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes
    """

    def parse(self, response):
        # for a in response.xpath('//div[@id="quotesList"]//div[@class="qll-bg"]'):
        for a in response.xpath('//div[@id="quotesList"]/div[contains(@id, "qpos_")]'):
            quote = a.xpath('.//a[@title="view quote"]/text()').get()
            author = a.xpath('.//a[@title="view author"]/text()').get()
            tags = a.xpath('.//div[@class="kw-box"]/a/text()').getall()
            url = a.xpath('.//a[@title="view quote"]//@href').get()
            yield {
                'quote': quote,
                'author': author,
                'tags': tags,
                'url': response.urljoin(url),
            }
        next_page = response.xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
