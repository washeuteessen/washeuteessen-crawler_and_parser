from ..items import RecipesItem
from ..items import RecipesHtml
import re
import scrapy
import subprocess
import urllib

class Chefkoch_htmlSpyder(scrapy.Spider):
    """ 
    This class scrapes www.chefkoch.de for recipes.

    CrawlingApproach:
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 30
    """
    # define name of spyder
    name = "chefkoch_html"

    # define start urls
    start_urls = ["https://www.chefkoch.de/rs/s0/Rezepte.html"]

    # define page number
    page_number = 30

    def parse(self, response):
        """
        Parse html reponse of scraper.

        Attributes:
            response (str): HTML source code of scraped page.

        Returns:
            items.json (dict): Json file with title and url of recipes as value.
        """
        # get all recipes 
        recipes = response.css("body > main > article")

        # iterate over recipes 
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_attr)

        # define url for next page
        next_page = "https://www.chefkoch.de/rs/s"+ str(Chefkoch_htmlSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # check if next page number is below threshold
        if Chefkoch_htmlSpyder.page_number <= 60:
            # increase page number by 30
            Chefkoch_htmlSpyder.page_number += 30

            # get response of next page
            yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        items = RecipesHtml()
        items["htmlbody"] = response.body()
        items["domain"] = self.name
        return items

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "recipes", "-s", "JOBDIR=crawls/recipes-1")