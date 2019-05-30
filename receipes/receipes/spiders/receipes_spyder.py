from ..items import ReceipesItem
import scrapy
import subprocess
import urllib

class ReceipesSpyder(scrapy.Spider):
    """ 
    This class scrapes desired url with pagination. 
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
            items.json (dict): Json file with title and url of receipes as value.
        """
        # instantiate items
        items = ReceipesItem()

        # get all receipes 
        all_receipes = response.css("body > main > article")

        # iterate over receipes 
        for receipe in all_receipes:
            # get title and url
            title = receipe.css("a::attr(data-vars-recipe-title)").extract_first()
            img_src = receipe.css("a figure amp-img::attr(src)").extract_first()
            url = receipe.css("a::attr(href)").extract_first()

            # store title and url as item
            items["title"] = title 
            items["img_src"] = img_src
            items["url"] = url

            # get items
            yield items

        # define url for next page
        next_page = "https://www.chefkoch.de/rs/s"+ str(ReceipesSpyder.page_number) + "e1n1z1b0i0m100000/Rezepte.html"
        
        # check if next page number is below threshold
        if ReceipesSpyder.page_number <= 60:
            # increase page number by 30
            ReceipesSpyder.page_number += 30

            # get response of next page
            yield response.follow(next_page, callback = self.parse)

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "receipes", "-s", "JOBDIR=crawls/receipes-1")