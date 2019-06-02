from ..items import RecipesItem
import os
import re
import scrapy
import subprocess
import urllib

class EatsmarterSpyder(scrapy.Spider):
    """ 
    This class scrapes domain Eatsmarter. 
    """
    # define name of spyder
    name = "eatsmarter"

    # define start urls
    start_urls = ["https://eatsmarter.de/suche/rezepte?ft=&op=Suchen&form_build_id=form-YbfzSni-wg3IicfsadcO_O9FSpmEEoQSfFhec4gsb94&form_id=eatsmarter_search_search_form"]

    # define page number
    page_number = 0

    def parse(self, response):
        """
        Parse html reponse of scraper.

        Attributes:
            response (str): HTML source code of scraped page.

        Returns:
            recipes_eatsmarter.json (dict): Json file with items dict.
        """
        # get all recipes 
        recipes = response.css(".tile")

        # iterate over recipes 
        for recipe in recipes:
            # extract information from html
            url = recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request("https://eatsmarter.de" + url, callback=self.parse_attr)

        # define url for next page
        next_page = f"https://eatsmarter.de/suche/rezepte?page={EatsmarterSpyder.page_number}&ft=&op=Suchen&form_build_id=form-YbfzSni-wg3IicfsadcO_O9FSpmEEoQSfFhec4gsb94&form_id=eatsmarter_search_search_form"
        
        # check if next page number is below threshold
        if ChefkochSpyder.page_number <= 10:
            # increase page number by 1
            ChefkochSpyder.page_number += 1

            # get response of next page
            yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css("h1::text").extract_first()

        # get title picture
        img_src = response.css("img.photo::attr(src)").extract_first()

        # initialize empty dict for ingredients
        ingredient_dict = {}

        # get name of ingredient
        ingredient_dict['name'] = response.css('a.name::text')

        # get amount of ingredient
        amount_amount = response.css('span.amount::text').extract()
        amount_type = response.css('span.type::text').extract()
        ingredient_dict["amount"] = 1 #" ".join(amount_amount, amount_type) 

        # get text
        steps = " ".join(response.css("div.preparation-step-items p::text").extract())

        # store information as item
        items["title"] = title 
        items["domain"] = self.name
        items["img_src"] = img_src
        items["ingredients"] = ingredient_dict
        items["url"] = response.url
        items["text"] = text

        return items