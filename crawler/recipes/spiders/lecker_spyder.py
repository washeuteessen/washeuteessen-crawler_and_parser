from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class LeckerSpyder(CrawlSpider):
    """
    This class scrapes www.lecker.de for recipes.

    CrawlingApproach:
    - go to start page
    - crawl all internal links
    - if url matches certain regex pattern identify url as recipe and extract content
    """
    # define name of spyder
    name = "lecker"

    # define start urls
    start_urls = ["https://www.lecker.de"]

    # define rule to only parse internal links
    rules = (Rule(LxmlLinkExtractor(allow_domains="lecker.de", allow="\d{5}.html$"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            items.json (dict): Json file with
                                - scraped url,
                                - domain name,
                                - html_body
                                of recipe as value.
        """
        # instantiate items
        items = RecipesItem()

        # store information as item
        items["url"] = response.url
        items["html_raw"] = response.text
        items["domain"] = self.name
        items["parsed_status"] = False

        return items
