from ..items import ReceipesItem
import scrapy

class ReceipesSpyder(scrapy.Spider):
    """ 
    This class scrapes desired urls. 
    """
    # define name of spyder
    name = "receipes"

    # define start urls
    start_urls = ["https://www.chefkoch.de/rezepte/"]
    #start_urls = ["https://www.heise.de/"]

    def parse(self, response):
        """
        Parse html reponse of scraper.

        Attributes:
            response (str): HTML source code of scraped page.

        Returns:
            title (dict): Dict with title of receipe as value.
        """
        # instantiate items
        items = ReceipesItem()

        # store information as item
        items["html_raw"] = response.body

        # get items
        yield items