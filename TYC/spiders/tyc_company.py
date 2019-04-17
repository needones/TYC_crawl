# -*- coding: utf-8 -*-
import scrapy


class TycCompanySpider(scrapy.Spider):
    name = 'tyc_company'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['http://www.tianyancha.com/']

    def parse(self, response):
        pass
