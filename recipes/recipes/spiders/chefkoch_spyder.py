import re
from ..items import RecipesItem
import scrapy
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
        next_page = "https://www.chefkoch.de/rs/s"+ str(ChefkochSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # increase page number by 30
        ChefkochSpyder.page_number += 30

        # get response of next page
        yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css(".page-title::text").extract_first()

        # get title picture
        img_src = response.css("a#0::attr(href)").extract_first()
        

        # get ingredients
        ingredients = response.xpath('//*[@id="recipe-incredients"]/div[1]/div[2]/table//tr')
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