# -*- coding: utf-8 -*-
"""
    Author: ychda
    Email: ychda@qq.com
    http://www.ychda.cn
"""
import scrapy


class Quotev2Spider(scrapy.Spider):
    name = 'quotev2'
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
            yield response.follow(url, callback=self.parse_author)

    """
    根据author主页
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes
    """

    def parse_author(self, response):
        for a in response.css('table.table a'):
            # author = a.xpath('./text()').get()
            url = response.urljoin(a.xpath('.//@href').get())
            yield response.follow(url, callback=self.parse_quote)
        if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
            page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
            for li in page_ul.xpath('.//li'):
                if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                    next_page = response.urljoin(li.xpath('.//a/@href').get())
                    yield response.follow(next_page, callback=self.parse_author)

    '''
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes的分页页面
    out: quote, author, tags, url
    查看html源码，可以看到分页显示有disable属性，但是不影响直接输入url来打开。
    '''

    def parse_quote(self, response):
        # for a in response.xpath('//div[@id="quotesList"]//a[@title="view quote"]'):
        for a in response.xpath('//div[@id="quotesList"]//div[@class="qll-bg"]'):
            quote = a.xpath('.//a[@title="view quote"]/text()').get()
            author = a.xpath('.//a[@title="view author"]/text()').get()
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
                    yield response.follow(next_page, callback=self.parse_quote)
