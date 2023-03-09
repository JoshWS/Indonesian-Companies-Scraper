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
        for page in range(1, 135502):
            url = f"https://companieshouse.id/?term=&page={page}"
            yield Request(
                url,
                callback=self.parse,
            )

    def parse(self, response):
        l = ItemLoader(item=CompanyScraperItem(), response=response)
        names = l.get_xpath(
            "//ul[@class='py-2 text-sm']/li/div/a[1]/@title",
            MapCompose(str.strip),
        )
        for name in names:
            l.add_value("name", name)

        return l.load_item()
