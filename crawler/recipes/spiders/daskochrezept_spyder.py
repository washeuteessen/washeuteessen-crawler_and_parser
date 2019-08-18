import re
from ..items import RecipesItem
import scrapy
import subprocess
import urllib

class DasKochrezeptSpyder(scrapy.Spider):
    """
    This class scrapes www.daskochrezept.de for recipes.

    CrawlingApproach:
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 1
    """
    # define name of spyder
    name = "daskochrezept"

    # define start urls
    start_urls = ['https://www.daskochrezept.de/suche?search=""&page=0']

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
        recipes = response.css("body > div.dialog-off-canvas-main-canvas > div.site-layout.site-layout--with-background > div.site-layout__page > main > div > div.layout-row.layout-row--bright.layout-row--no-torned-edge-top\@mobile.layout-row--torned-edge.layout-row--unconstrained\@mobile > div > div > div > main > div > div > div.views-element-container > div > div > ul > li:nth-child(1) > div")
        # not working yet

        # iterate over recipes
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

        # define url for next page
        next_page = 'https://www.daskochrezept.de/suche?search=""&page='+ str(DasKochrezeptSpyder.page_number)

        # increase page number by 1
        DasKochrezeptSpyder.page_number += 1

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
