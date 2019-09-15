import re
from ..items import RecipesItem
import scrapy
from scrapy.exceptions import CloseSpider
import subprocess
import urllib

class ChefkochSpyder(scrapy.Spider):
    """
    This class scrapes www.chefkoch.de for recipes.

    CrawlingApproach:
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 30
    - stop scraper, if page number 11.006 alias 330.180 is reached
    """
    # define name of spyder
    name = "chefkoch"

    # define start urls
    start_urls = ["https://www.chefkoch.de/rs/s0/Rezepte.html"]

    # define page number
    page_number = 30

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            call to follow next page
        """
        # get all recipes
        recipes = response.css("body > main > article")

        # iterate over recipes
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

        # define url for next page
        next_page = "https://www.chefkoch.de/rs/s"+ str(ChefkochSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"

        # increase page number by 30
        ChefkochSpyder.page_number += 30

        # check whether specific page (probably last page with content) has been reached and close spider
        max_page_number = 330180
        
        if ChefkochSpyder.page_number == max_page_number:
            raise CloseSpider(reason = f"Max. pagenumber of {max_page_number} reached. No more recipes to crawl.")

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
