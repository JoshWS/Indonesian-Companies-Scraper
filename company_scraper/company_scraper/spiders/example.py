from dateutil.parser import parse
from itemloaders.processors import Join, MapCompose
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

# from news_scrapers.helpers import clean_html, re_replace, remove_tags
# from news_scrapers.items import NewsScrapersItem


class BangkokPostSpider(Spider):
    # Spider name.
    name = "bangkokpost"
    # Add site_name attribute for Item Pipeline
    site_name = "Bangkok Post"
    # Add site_short_name attribute for Item Pipeline
    site_short_name = "BangkokPost"
    # Add site_url attribute for Item Pipeline
    site_url = "https://www.bangkokpost.com"
    # Add site language for Item Pipeline.
    language = "English"
    # Use a file with urls to scrape from the crawl command.
    # For example: scrapy crawl dica -a file=dicaurls.txt
    file = None
    # Used in pipeline to disable checking of text and html.
    # Allow an empty body.
    allow_empty_body = False

    allowed_domains = ["www.bangkokpost.com"]

    def start_requests(self):
        if self.file:
            with open(self.file) as f:
                urls = [url.strip() for url in f.readlines()]

            for url in urls:
                yield Request(url, callback=self.parse_article)
        else:
            urls = [
                "https://www.bangkokpost.com/topstories",
                "https://www.bangkokpost.com/most-recent/",
                "https://www.bangkokpost.com/news/politics",
                "https://www.bangkokpost.com/news/crime",
                "https://www.bangkokpost.com/news/general",
                "https://www.bangkokpost.com/news/asean",
                "https://www.bangkokpost.com/news/special-reports",
                "https://www.bangkokpost.com/news/security",
                "https://www.bangkokpost.com/news/transport",
                "https://www.bangkokpost.com/news/environment",
            ]
            for url in urls:
                yield Request(url, callback=self.parse)

    def parse(self, response):
        # Follow links to articles
        article_selector = response.xpath("//*/div[@class='detail']/h3/a/@href")
        for article in article_selector:
            yield response.follow(article, self.parse_article)

        # follow pagination links
        next_page = response.xpath("//a[text()='Next']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        l = ItemLoader(item=NewsScrapersItem(), response=response)
        # Add the article url
        l.add_value("url", response.url)

        # Get article title
        l.add_xpath(
            "title", "//meta[@property='og:title']/@content", MapCompose(str.strip)
        )

        # Article date
        l.add_xpath(
            "date",
            "//*/span[@itemprop='datePublished']/text()",
            MapCompose(lambda i: str(parse(i).date())),
        )

        # Get article text
        text = l.get_xpath(
            "//*/div[@class='articleContents']/p/text()",
            MapCompose(str.strip),
            Join(""),
        )
        if text:
            text = clean_html(text)
            text = remove_tags(text)
            text = re_replace(text, "<p>")
            text = re_replace(text, "</p>")
            l.add_value("text", text)

        # Get article text with basic html intact
        html = l.get_xpath(
            "//*/div[@class='articleContents']/p", MapCompose(str.strip), Join("")
        )
        if html:
            html = clean_html(html)
            html = remove_tags(html)
            l.add_value("html", html)

        # Get Images and caption.
        if l.get_xpath("//meta[@property='og:image']/@content"):
            image = l.get_xpath("//meta[@property='og:image']/@content")
            if "nopic" not in image[0]:
                l.add_value("image_url", image)

        return l.load_item()