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
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 1
    """
    # define name of spyder
    name = "womenshealth"

    # define start urls
    start_urls = ["https://www.womenshealth.de/food/gesunde-rezepte/page/1?s="]

    # define page number
    page_number = 1

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            call to follow next page
        """
        # get all recipes
        recipes = response.css("body > div.v-A_-wrapper--stroer > div.v-A_-wrapper.v-A_-clear > div.v-A_-maincol > div > div")

        # iterate over recipes
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

        # define url for next page
        next_page = "https://www.womenshealth.de/food/gesunde-rezepte/page/"+ str(WomenshealthSpyder.page_number) + "?s="

        # increase page number by 1
        WomenshealthSpyder.page_number += 1

        # get response of next page
        yield response.follow(next_page, callback = self.parse)

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
