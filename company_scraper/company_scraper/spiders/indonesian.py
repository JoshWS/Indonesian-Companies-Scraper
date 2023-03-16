from dateutil.parser import parse
from itemloaders.processors import Join, MapCompose
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
import string

# from news_scrapers.helpers import clean_html, re_replace, remove_tags
from company_scraper.items import CompanyScraperItem


class IndonesianSpider(Spider):
    name = "indonesian"
    allowed_domains = ["companieshouse.id"]

    def start_requests(self):
        with open("company_scraper/search_terms.txt") as f:
            terms = f.readlines()
        for term in terms:
            term = term.replace("\n", "")
            url = f"https://companieshouse.id/?term={term}"
            yield Request(
                url, callback=self.parse, errback=self.errback, dont_filter=True
            )

        # alpha = list(string.ascii_lowercase)
        # alpha.reverse()
        # alpha = alpha[:5]
        # for letter1 in alpha:
        #     for letter2 in alpha:
        #         for letter3 in alpha:
        #             url = f"https://companieshouse.id/?term={letter1}{letter2}{letter3}"
        #             yield Request(
        #                 url, callback=self.parse, errback=self.errback, dont_filter=True
        #             )

    def parse(self, response):
        yield self.parse_pages(response)
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(
                next_page, callback=self.parse, errback=self.errback, dont_filter=True
            )

    def parse_pages(self, response):
        l = ItemLoader(item=CompanyScraperItem(), response=response)
        names = l.get_xpath(
            "//ul[@class='py-2 text-sm']/li/div/a[1]/@title",
            MapCompose(str.strip),
        )
        if names:
            for name in names:
                l.add_value("name", name)
        else:
            return

        return l.load_item()

    def errback(self, failure):
        yield Request(
            failure.value.response.url,
            callback=self.parse,
            errback=self.errback,
            dont_filter=True,
        )
