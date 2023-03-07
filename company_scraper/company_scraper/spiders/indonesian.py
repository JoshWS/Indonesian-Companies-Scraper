from dateutil.parser import parse
from itemloaders.processors import Join, MapCompose
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

# from news_scrapers.helpers import clean_html, re_replace, remove_tags
# from news_scrapers.items import NewsScrapersItem

class IndonesianSpider(Spider):
    name = 'indonesian'
    allowed_domains = ['companieshouse.id']
    
    def start_requests(self):
        for page in range(1, 3):
            url = f"https://companieshouse.id/?term=&page={page}"
            print("START REQUEST")
            yield Request(url, callback=self.parse)
            
    def parse(self, response):
        print("___________________________")
        print("SCRAPED")
        print("___________________________")