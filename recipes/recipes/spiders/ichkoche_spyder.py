from ..items import RecipesItem
import re
import scrapy
import subprocess
import urllib

class IchkocheSpyder(scrapy.Spider):
    """ 
    This class scrapes www.ichkoche.at for recipes.

    CrawlingApproach:
    - start at recipe A-Z listing
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 1
    """
    # define name of spyder
    name = "ichkoche"

    # define start urls
    start_urls = ["https://www.ichkoche.at/rezepte-az"]

    # define page number
    page_number = 30

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            items.json (dict): Json file with 
                                - title, 
                                - domain name, 
                                - image url, 
                                - list of ingredients, 
                                - url and 
                                - description text
                                of recipe as value.
        """
        # get all recipes 
        recipes = response.css("body > main > article")

        # iterate over recipes 
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_attr)

        # define url for next page
        next_page = "https://www.chefkoch.de/rs/s"+ str(IchkocheSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # check if next page number is below threshold
        if IchkocheSpyder.page_number <= 2100000:
            # increase page number by 30
            IchkocheSpyder.page_number += 30

            # get response of next page
            yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        # instantiate items
        items = RecipesItem()

        # store information as item
        items["url"] = response.url
        items["html_raw"] = response.body
        items["domain"] = self.name

        return items