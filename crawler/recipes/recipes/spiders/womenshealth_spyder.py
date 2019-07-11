from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class WomenshealthSpyder(CrawlSpider):
    """ 
    This class scrapes www.womenshealth.de for recipes.

    CrawlingApproach:
    - start with subpage dedicated to food
    - crawl all internal links
    - if url matches certain regex pattern identify url as recipe and extract content
    """
    # define name of spyder
    name = "womenshealth"

    # define start urls
    start_urls = ["https://www.womenshealth.de/food/gesunde-rezepte/"]

    # define rule to only parse internal links 
    rules = (Rule(LxmlLinkExtractor(allow_domains="womenshealth.de"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
        ------------
            items.json (dict): Json file with 
                                - domain name, 
                                - html_body
                                of recipe as value.
        """

        # instantiate items
        items = RecipesItem()

        # store information as item
        items["url"] = response.url
        items["html_raw"] = response.body
        items["domain"] = self.name

        return items