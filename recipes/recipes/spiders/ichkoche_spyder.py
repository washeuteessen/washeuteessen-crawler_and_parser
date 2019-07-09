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
    page_number = 1

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
            url = "https://www.ichkoche.at" + recipe.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_attr)

        # define url for next page
        next_page = "https://www.ichkoche.at/rezepte-az?page="+ str(ChefkochSpyder.page_number) 
        
        # increase page number by 1
        IchkocheSpyder.page_number += 1

        # get response of next page
        yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css(".page-title::text").extract_first()

        # get title picture
        # TODO: img src
        img_src = response.css("a#0::attr(href)").extract_first()


        # get ingredients
        # TODO: ingredients fertig stellen
        ingredients = response.css('.ingredient').extract()
        ingredients_list = []
        for ingredient in ingredients:
            # get name of ingredient
            if len(ingredient.xpath('td[2]//text()').extract_first().strip()) > 1:
                ingredient = ingredient.xpath('td[2]//text()').extract_first().strip()
            else:
                ingredient = ingredient.xpath('td[2]/a/text()').extract_first().strip()

            # append ingredient dict to ingredients list
            ingredients_list.append(ingredient)

        # get text
        # TODO: text extrahieren
        text = re.sub(" +", " ", " ".join(response.css("#rezept-zubereitung::text").extract()) \
                        .replace("\n", " ").replace("\r", " ")) \
                        .strip()

        # store information as item
        items["title"] = title 
        items["domain"] = self.name
        items["img_src"] = img_src
        items["ingredients"] = ingredients_list
        items["url"] = response.url
        items["text"] = text

        return items
