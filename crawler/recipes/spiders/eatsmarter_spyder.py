from ..items import RecipesItem
import logging
import os
import re
import scrapy
import subprocess
import urllib

class EatsmarterSpyder(scrapy.Spider):
    """
    This class scrapes www.eatsmarter.de for recipes.

    CrawlingApproach:
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 1
    """
    # define name of spyder
    name = "eatsmarter"

    # define start urls
    start_urls = ["https://eatsmarter.de/suche/rezepte?ft=&op=Suchen&form_build_id=form-YbfzSni-wg3IicfsadcO_O9FSpmEEoQSfFhec4gsb94&form_id=eatsmarter_search_search_form"]

    # define page number
    page_number = 0

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            call to follow next page
        """
        # get all recipes
        recipes = response.css(".tile")

        # iterate over recipes
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            try:
                yield scrapy.Request("https://eatsmarter.de" + url, callback=self.parse_item)
            except TypeError as e:
                logging.info(e)

        # define url for next page
        next_page = f"https://eatsmarter.de/suche/rezepte?page={EatsmarterSpyder.page_number}&ft=&op=Suchen&form_build_id=form-YbfzSni-wg3IicfsadcO_O9FSpmEEoQSfFhec4gsb94&form_id=eatsmarter_search_search_form"

        # increase page number by 1
        EatsmarterSpyder.page_number += 1

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
