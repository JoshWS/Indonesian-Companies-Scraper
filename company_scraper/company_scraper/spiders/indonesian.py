from dateutil.parser import parse
from itemloaders.processors import Join, MapCompose
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from scrapy.exceptions import IgnoreRequest
import string

# from news_scrapers.helpers import clean_html, re_replace, remove_tags
from company_scraper.items import CompanyScraperItem

GENERATE_TERMS = False


class IndonesianSpider(Spider):
    name = "indonesian"
    allowed_domains = ["companieshouse.id"]

    def start_requests(self):
        if GENERATE_TERMS == False:
            with open("company_scraper/search_terms.txt") as f:
                terms = f.readlines()
            for term in terms:
                term = term.replace("\n", "")
                url = f"https://companieshouse.id/?term={term}"
                yield Request(
                    url, callback=self.parse, errback=self.errback, dont_filter=True
                )
        else:
            alpha = list(string.ascii_lowercase)
            alpha.reverse()
            alpha_stop = alpha[:18]
            alpha_all = alpha
            with open("company_scraper/search_terms.txt") as f:
                terms = f.readlines()
                with open("company_scraper/skip_terms.txt") as g:
                    skip = g.readlines()
                    print(skip)
                for letter1 in alpha_stop:
                    for letter2 in alpha_all:
                        for letter3 in alpha_all:
                            term = f"{letter1}{letter2}{letter3}"
                            if f"{term}\n" not in terms:
                                if f"{term}\n" not in skip:
                                    url = f"https://companieshouse.id/?term={term}"
                                    yield Request(
                                        url,
                                        callback=self.parse,
                                        errback=self.errback,
                                        dont_filter=True,
                                    )

    def parse(self, response):
        yield self.parse_pages(response)
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                errback=self.errback,
                dont_filter=True,
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
            with open("company_scraper/skip_terms.txt", "a") as f:
                skip = response.request.url[-3:]
                f.write(f"{skip}\n")
            return

        return l.load_item()

    def errback(self, failure):
        if not IgnoreRequest:
            yield Request(
                failure.value.response.url,
                callback=self.parse,
                errback=self.errback,
                dont_filter=True,
            )
