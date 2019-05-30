from ..items import RecipesItem
import scrapy
import subprocess
import urllib

class RecipesSpyder(scrapy.Spider):
    """ 
    This class scrapes desired url with pagination. 
    """
    # define name of spyder
    name = "recipes"

    # define start urls
    start_urls = ["https://www.chefkoch.de/rs/s0e1n1z1b0i0m100000/Rezepte.html"]

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

        # # define url for next page
        # next_page = "https://www.chefkoch.de/rs/s"+ str(recipesSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # # check if next page number is below threshold
        # if recipesSpyder.page_number <= 60:
        #     # increase page number by 30
        #     recipesSpyder.page_number += 30

        #     # get response of next page
        #     yield response.follow(next_page, callback = self.parse)

    def parse_attr(self, response):
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css(".page-title::text").extract_first()

        #
        # img_src = recipe.css("a figure amp-img::attr(src)").extract_first()

        # get ingredients
        ingredients = response.xpath('//*[@id="recipe-incredients"]/div[1]/div[2]/table//tr')
        ingredients_dict = {}
        ingredients_dict['amount'] = [ingredient.xpath('td[1]//text()').extract_first().strip() for ingredient in ingredients]
        ingredients_dict['ingredient'] = [ingredient.xpath('td[2]//text()').extract_first().strip() \
                                            if len(ingredient.xpath('td[2]//text()').extract_first().strip()) > 1 \
                                            else ingredient.xpath('td[2]/a/text()').extract_first().strip() \
                                            for ingredient in ingredients]

        # desired scheme
        # {"ingridients" : [
        #     { 
        #         "name": "Test",
        #         "amount": "300g"
        #     },
        #     {
        #         "name": "Test2",
        #         "amount": "5kg"
        #     }
        #     ]
        #     }

        # get text
        text = " ".join(response.css("#rezept-zubereitung::text").extract()) \
                        .replace("\n", " ").replace("\r", " ") \
                        .re.sub(' +', ' ')

        # store information as item
        items["title"] = title 
        # items["img_src"] = img_src
        items["ingredients"] = ingredients_dict
        items["url"] = response.url
        items["text"] = text

        return items

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "recipes", "-s", "JOBDIR=crawls/recipes-1")