import datetime
import logging
import os

from scrapy import signals
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.utils.project import data_path
from sqlitedict import SqliteDict

logger = logging.getLogger(__name__)


class CrawlOnceMiddleware:
    """
    This spider and downloader middleware allows to avoid re-crawling pages
    of items that already have been scraped and has passed all the Item Pipeline stages (without being dropped).
    Based on: https://github.com/TeamHG-Memex/scrapy-crawl-once and https://github.com/scrapy-plugins/scrapy-deltafetch


    To enable it, modify your settings.py::

        SPIDER_MIDDLEWARES = {
            # ...
            'envisage_scrapers.crawl-once.CrawlOnceMiddleware': 100,
            # ...
        }

        DOWNLOADER_MIDDLEWARES = {
            # ...
            'envisage_scrapers.crawl_once.CrawlOnceMiddleware': 50,
            # ...
        }

    Settings:

    * ``CRAWL_ONCE_ENABLED`` - set it to False to disable middleware.
      Default is True.
    * ``CRAWL_ONCE_PATH`` - a path to a folder with crawled requests database.
      By default ``.scrapy/crawl_once/`` path is used; this folder contains
      ``<spider_name>.sqlite`` files with databases of seen requests.
    * ``CRAWL_ONCE_RESET`` - reset the state, clearing out all seen requests
    """

    def __init__(self, path, stats, crawler, reset=False):
        self.path = path
        self.stats = stats
        self.reset = reset
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool("CRAWL_ONCE_ENABLED", True):
            raise NotConfigured()
        path = data_path(s.get("CRAWL_ONCE_PATH", "crawl_once"), createdir=True)
        reset = s.getbool("CRAWL_ONCE_RESET")
        o = cls(path, crawler.stats, crawler, reset)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o._item_scraped, signal=signals.item_scraped)
        return o

    def spider_opened(self, spider):
        self.db, dbpath = self._spider_db(spider)
        num_records = len(self.db)
        logger.info(
            "Opened crawl database %r with %d existing records" % (dbpath, num_records)
        )
        self.stats.set_value("crawl_once/initial", num_records)

    def spider_closed(self, spider):
        self.db.close()

    def _spider_db(self, spider):
        dbpath = os.path.join(self.path, "%s.sqlite" % spider.name)
        if self.reset:
            flag = "w"
        else:
            flag = "c"
        db = SqliteDict(
            filename=dbpath, tablename="requests", autocommit=True, flag=flag
        )
        return db, dbpath

    def _get_key(self, request):
        return request.meta.get(
            "crawl_once_key"
        ) or self.crawler.request_fingerprinter.fingerprint(request)

    # spider middleware interface
    def _item_scraped(self, item, response, spider):
        # response is crawled, store its fingerprint in DB if crawl_once
        # is requested.
        key = self._get_key(response.request)
        self.db[key] = datetime.datetime.now()
        self.stats.inc_value("crawl_once/stored")

    # downloader middleware interface
    def process_request(self, request, spider):
        if self._get_key(request) in self.db:
            self.stats.inc_value("crawl_once/ignored")
            raise IgnoreRequest()
