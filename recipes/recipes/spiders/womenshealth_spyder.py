from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class WomenshealthSpyder(CrawlSpider):
    """ 
    This class scrapes www.womenshealth.de for recipes.

    CrawlingApproach:
    - start with subpage dedicated to food
    - crawl all internal links
    - if url matches certain regex pattern identify url as recipe and extract content
    """
    # define name of spyder
    name = "womenshealth"

    # define start urls
    start_urls = ["https://www.womenshealth.de/food/gesunde-rezepte/"]

    # define rule to only parse internal links 
    rules = (Rule(LxmlLinkExtractor(allow_domains="womenshealth.de"), callback="parse_item", follow=True),)

    def parse_item(self, response):
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
        # instantiate items
        items = RecipesItem()

        # check if url contains a recipe
        if re.search(pattern="-rezept.[0-9]{6,7}.html", string=response.url) is not None:

            # get recipe title
            title = response.css(".v-A_-headline--ad::text").extract()[-1]
            title = title.strip()

            # get title picture
            img_src = response.css(".v-A_-article__hero__image > img:nth-child(1)::attr(src)").extract_first()

            # get ingredients
            ingredients = response.css("ul li::text").extract()

            # strip \n
            ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

            # strip whitespace
            ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
            ingredients = [ingredient.strip() for ingredient in ingredients]

            # strip empty list elemens
            ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

            # get text
            text = " ".join(response.css(".rdb-instructions li::text").extract())

            # store information as item
            items["title"] = title 
            items["domain"] = self.name
            items["img_src"] = img_src
            items["ingredients"] = ingredients
            items["url"] = response.url
            items["text"] = text

        else:
            pass

        return items