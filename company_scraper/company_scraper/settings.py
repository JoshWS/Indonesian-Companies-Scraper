# Scrapy settings for company_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "company_scraper"

SPIDER_MODULES = ["company_scraper.spiders"]
NEWSPIDER_MODULE = "company_scraper.spiders"


FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",  # This is the first provider we'll try
    "scrapy_fake_useragent.providers.FakerProvider",  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",  # Fall back to USER_AGENT value
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'company_scraper.middlewares.CompanyScraperSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "company_scraper.crawl-once.CrawlOnceMiddleware": 50,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 450,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
}

ENABLE_ROTATING_PROXIES = False
if ENABLE_ROTATING_PROXIES:
    DOWNLOADER_MIDDLEWARES["rotating_proxies.middlewares.RotatingProxyMiddleware"] = 555
    DOWNLOADER_MIDDLEWARES["rotating_proxies.middlewares.BanDetectionMiddleware"] = 556

# scrapy-rotating-proxies settings.
# https://github.com/TeamHG-Memex/scrapy-rotating-proxies
# path to a file with a list of proxies
ROTATING_PROXY_LIST_PATH = "./proxies.txt"
# a number of times to retry downloading a page using a different proxy.
# After this amount of retries failure is considered a page failure, not a proxy failure.
# Think of it this way: every improperly detected ban cost you
# ROTATING_PROXY_PAGE_RETRY_TIMES alive proxies. Default: 5.
ROTATING_PROXY_PAGE_RETRY_TIMES = 15
# stats logging interval in seconds, 30 by default;
ROTATING_PROXY_LOGSTATS_INTERVAL = 15
# base backoff time, in seconds. Default is 300 (i.e. 5 min).
ROTATING_PROXY_BACKOFF_BASE = 300
# backoff time cap, in seconds. Default is 3600 (i.e. 60 min).
ROTATING_PROXY_BACKOFF_CAP = 1200


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "company_scraper.mongo.MongoDBPipeline": 500,
}


FEED_EXPORT_FIELDS = ["name"]


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
