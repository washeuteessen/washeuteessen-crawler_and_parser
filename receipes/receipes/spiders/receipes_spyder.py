from ..items import ReceipesItem
import scrapy

class ReceipesSpyder(scrapy.Spider):
    """ 
    This class scrapes desired urls. 
    """
    # define name of spyder
    name = "receipes"

    # define start urls
    start_urls = ["https://www.chefkoch.de/rs/s0e1n1z1b0i0m100000/Rezepte.html"]

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

        # get title, url
        title = response.css(".ds-h3.ds-heading-link::text").extract()
        url = response.css("body > main > article > a::attr(href)").extract()

        # store information as item
        items["title"] = title
        items["url"] = url

        # get items
        yield items