from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib
import base64


class LeckerSpyder(scrapy.Spider):
    """
    This class scrapes www.lecker.de for recipes.

    CrawlingApproach:
    - start at recipe search which lists all recipes
    - extract url of each recipe step by step
    - go to each recipe url and extract content
    - go to next page by incrementing page number by 1
    """
    # define name of spyder
    name = "lecker"

    # define start urls
    start_urls = ["https://www.lecker.de/suche-rezept/*"]

    # custom_settings enable java script
    

    # define page number
    page_number = 1

    def parse(self, response):
        """
        Parse html response of scraper.

        Attributes:
            response (str): response object of HTML request.

        Returns:
            call to follow next page
        """
        # get all recipes
        links = response.css("recipe-search-hit")

        # iterate over recipes
        for link in links:
            # extract information from html         
            url = "https://www.lecker.de" + link.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

        # define url for next page
        props = '{"lastSearch":"*","offset":"&offset='+str((LeckerSpyder.page_number-1)*10)+'","sort":"score","checkboxes":{"meal":{"selection":[],"hasFacet":[],"facets":"true"},"course":{"selection":[],"hasFacet":[],"facets":"true"},"dietaryConsiderations":{"selection":[],"hasFacet":[],"facets":"true"},"cuisine":{"selection":[],"hasFacet":[],"facets":"true"},"publication":{"selection":[],"facets":"false"}},"slider":{"time":{"value":120},"calories":{"value":120}}}'
        props_encoded = base64.b64encode(bytes(props,encoding="utf-8"))
        next_page = "https://www.lecker.de/suche-rezept/*?search=" + str(props_encoded).rstrip("'")[2:] + "#js-search"

        # increase page number by 30
        LeckerSpyder.page_number += 1

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
