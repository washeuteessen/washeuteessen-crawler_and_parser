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

    # define page number
    page_number = 1

    # define start urls
    start_urls = ["https://www.ichkoche.at/rezepte-az?page=1"]

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            call to follow next page
        """
        # get all recipes
        recipes = response.xpath("//article/div/h3")

        # iterate over recipes
        for recipe in recipes:
            # extract information from html
            url = "https://www.ichkoche.at" + recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

        # define url for next page
        next_page = "https://www.ichkoche.at/rezepte-az?page="+ str(IchkocheSpyder.page_number)

        # increase page number by 1
        IchkocheSpyder.page_number += 1

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

        return items
