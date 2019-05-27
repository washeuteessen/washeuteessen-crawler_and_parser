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

    # define page number
    page_number = 30

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

        # get all receipes 
        all_receipes = response.css("body > main > article")

        # iterate over receipes 
        for receipe in all_receipes:
            # get title and url
            title = receipe.css("a::attr(data-vars-recipe-title)").extract()
            url = receipe.css("a::attr(href)").extract()

            # store title and url as item
            items["title"] = title
            items["url"] = url

            # get items
            yield items

        # define url for next page
        next_page = "https://www.chefkoch.de/rs/s"+ str(ReceipesSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # check if next page number is below threshold
        if ReceipesSpyder.page_number <= 100:
            # increase page number by 30
            ReceipesSpyder.page_number += 30

            # get response of next page
            yield response.follow(next_page, callback = self.parse)