# -*- coding: utf-8 -*-
"""
    Author: ychda
    Email: ychda@qq.com
    http://www.ychda.cn
"""
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'all_author'
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
            author = a.xpath('./text()').get()
            url = response.urljoin(a.xpath('.//@href').get())
            yield {
                'author': author,
                'url': url,
            }
            """
            # 27845
            if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
                page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
                for li in page_ul.xpath('.//li'):
                    if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                        next_page = response.urljoin(li.xpath('.//a/@href').get())
                        yield response.follow(next_page, callback=self.parse_author)
            """
            next_page = response.xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),"Next")]/@href').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_author)
