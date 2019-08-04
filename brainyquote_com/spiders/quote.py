# -*- coding: utf-8 -*-
"""
    Author: ychda
    Email: ychda@qq.com
    http://www.ychda.cn
"""
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com']

    """
    in: https://www.brainyquote.com
    """

    def parse(self, response):
        urls = response.xpath('//span[@class="body bq-tn-letters"]/span[@class="bq-tn-wrap"]/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            yield response.follow(url, callback=self.parse_author)

    """
    in: https://www.brainyquote.com/authors/a-boogie-wit-da-hoodie-quotes
    """

    def parse_author(self, response):
        for a in response.css('table.table a'):
            # author = a.xpath('./text()').get()
            url = response.urljoin(a.xpath('.//@href').get())
            yield response.follow(url, callback=self.parse_quote)
        next_page = response.xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
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
                'quote': quote,
                'author': author,
                'tags': tags,
                'url': response.urljoin(url),
            }
        """
        if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
            page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
            for li in page_ul.xpath('.//li'):
                if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                    next_page = response.urljoin(li.xpath('.//a/@href').get())
                    yield response.follow(next_page, callback=self.parse_quote)
        """
        next_page = response.xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_author)
