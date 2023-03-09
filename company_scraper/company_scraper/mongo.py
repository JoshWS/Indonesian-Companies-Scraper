# https://github.com/VigilantePolitico/vigilante/raw/9935c2821e4ad17e083bf22ea237d379ffbda8cb/vigilante/pipelines/mongo.py
import pymongo
import sys
from .items import CompanyScraperItem


class MongoDBPipeline:
    collection = "scrapy_items"

    @classmethod
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["companies"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(CompanyScraperItem(item))
        self.db[self.collection].insert_one(data)
        return item
