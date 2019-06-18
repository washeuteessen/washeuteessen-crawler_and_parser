from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class EssenundtrinkenSpyder(CrawlSpider):
    """ 
    This class scrapes www.essen-und-trinken.de for recipes.

    CrawlingApproach:
    - start at main page
    - follow all internal links
    - if url matches certain regex pattern identify url as recipe and extract content
    """
    # define name of spyder
    name = "essenundtrinken"

    # define start urls
    start_urls = ["https://www.essen-und-trinken.de"]

    # define rule to only parse internal links 
    rules = (Rule(LxmlLinkExtractor(allow_domains="essen-und-trinken.de"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
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

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "recipes", "-s", "JOBDIR=crawls/recipes-1")