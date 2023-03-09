# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class CompanyScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
