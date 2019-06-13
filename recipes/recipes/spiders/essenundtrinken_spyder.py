from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class ChefkochSpyder(CrawlSpider):
    """ 
    This class scrapes desired url by searching for recipe urls. 
    """
    # define name of spyder
    name = "essenundtrinken"

    # define start urls
    start_urls = ["https://www.essen-und-trinken.de"]

    # define rule to only parse links with "rezepte"
    #TODO: expand rule to follow more than one depth
    rules = (Rule(LxmlLinkExtractor(allow="/rezepte/[0-9]{5}-*"), callback="parse_item"),)

    def parse_item(self, response):
        """
        Parse html reponse of scraper.

        Attributes:
            response (str): HTML source code of scraped page.

        Returns:
            items.json (dict): Json file with title and url of recipes as value.
        """
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css(".headline-title::text").extract_first()

        # TODO: check why some times image source is not found
        # get title picture
        img_src = response.css(".recipe-img > img:nth-child(1)::attr(src)").extract_first()

        # get ingredients
        # (".ingredients-list li")

        # get text
        #TODO: check why some texts are not scraped
        text = " ".join(response.css("ul.preparation li.preparation-step div.preparation-text p::text").extract())

        # store information as item
        items["title"] = title 
        items["domain"] = self.name
        items["img_src"] = img_src
        # items["ingredients"] = ingredients_list
        items["url"] = response.url
        items["text"] = text

        return items

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "recipes", "-s", "JOBDIR=crawls/recipes-1")