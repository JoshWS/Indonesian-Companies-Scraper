from dateutil.parser import parse
from itemloaders.processors import Join, MapCompose
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from scrapy.spidermiddlewares.httperror import HttpError

# from news_scrapers.helpers import clean_html, re_replace, remove_tags
from company_scraper.items import CompanyScraperItem


class IndonesianSpider(Spider):
    name = "indonesian"
    allowed_domains = ["companieshouse.id"]

    def start_requests(self):
    #   135502
        for page in range(1, 11):
            url = f"https://companieshouse.id/?term=&page={page}"
            print("START REQUEST")
            yield Request(
                url,
                callback=self.parse,
            )

    def parse(self, response):
        l = ItemLoader(item=CompanyScraperItem(), response=response)
        l.add_xpath(
            "name",
            "//ul[@class='py-2 text-sm']/li/div/a[1]/@title",
            MapCompose(str.strip),
        )
        return l.load_item()
