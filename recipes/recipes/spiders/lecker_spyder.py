from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class LeckerSpyder(CrawlSpider):
    """ 
    This class scrapes www.lecker.de for recipes.

    CrawlingApproach:
    - go to start page
    - crawl all internal links
    - if url matches certain regex pattern identify url as recipe and extract content
    """
    # define name of spyder
    name = "lecker"

    # define start urls
    start_urls = ["https://www.lecker.de"]

    # define rule to only parse internal links 
    rules = (Rule(LxmlLinkExtractor(allow_domains="lecker.de"), callback="parse_item", follow=True),)

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
        if re.search(pattern="-[0-9]{5}.html$", string=response.url) is not None and re.search(pattern="datenschutzerklaerung", string=response.url) is None:

            # get recipe title
            title = response.css("h1::text").extract_first()
    
            # get title picture
            img_src = response.css(".article-figure--default-image img::attr(src)").extract_first()

            # version A of recipe presentation
            if img_src is not None:
                # get ingredients
                ingredients = response.css(".ingredientBlock::text").extract()

                # get text
                text = " ".join(response.css("dd::text").extract())
                
                # strip \n
                text = re.sub("\n", "", text)

                # strip whitespace
                text = re.sub(" +", " ", text)
                text = text.strip()

            # version B of recipe presentation 
            else:
                # get url of main image
                img_src = response.css(".typo--editor+ .article-figure--fullsize img::attrc(src)")

                # get ingredients
                ingredients = response.css("h2+ ul li::text").extract()

                # get text
                text = "no_distinct_text_available"

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