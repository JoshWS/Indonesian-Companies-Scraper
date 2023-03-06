import scrapy


class IndonesianSpider(scrapy.Spider):
    name = 'indonesian'
    allowed_domains = ['companieshouse.id']
    start_urls = ['http://companieshouse.id/']

    def parse(self, response):
        pass
