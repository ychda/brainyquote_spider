# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com/authors']

    def parse(self, response):
        urls = response.css('h2.indexContentHeader a::attr(href)').getall()
        urls.append('https://www.brainyquote.com/authors/x')
        for url in urls:
            yield response.follow(url, self.parse_az)

    def parse_az(self, response):
        url = response.url
        yield SplashRequest(url, callback=self.parse_author, args={'wait': 0.5})

    def parse_author(self, response):
        for a in response.css('table.table a'):
            author = a.xpath('./text()').get()
            url = response.urljoin(a.xpath('.//@href').get())

            yield {
                'author': author,
                'url': url,
            }

        """
        page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
        for li in page_ul.xpath('.//li'):
            if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                print(li.xpath('.//a/@href').get())
        """
        if response.xpath('//ul[contains(@class,"pagination")]').get() is not None:
            page_ul = response.xpath('//ul[contains(@class,"pagination")]')[0]
            for li in page_ul.xpath('.//li'):
                if li.xpath('.//a/text()').get() == 'Next' and li.xpath('.//a') is not None:
                    next_page = response.urljoin(li.xpath('.//a/@href').get())
                    yield SplashRequest(next_page, callback=self.parse_author, args={'wait': 0.5})
