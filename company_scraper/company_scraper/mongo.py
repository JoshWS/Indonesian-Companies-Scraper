# https://github.com/VigilantePolitico/vigilante/raw/9935c2821e4ad17e083bf22ea237d379ffbda8cb/vigilante/pipelines/mongo.py
import logging
from mongoengine import connect
from itemadapter import ItemAdapter

logger = logging.getLogger("mongo")


class MongoDBPipeline(object):
    collection = "scrapy_items"

    def __init__(self):
        self.ids_seen = set()

    @classmethod
    def open_spider(self, spider):
        logger.info("Connecting to mongodb://localhost:27017")
        self.client = connect(db="companies", host="mongodb://localhost:27017")
        self.db = self.client["companies"]
        logger.debug("Connected")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].update_one(
            {"name": item["name"]}, {"$set": ItemAdapter(item)}, upsert=True
        )
        return item
