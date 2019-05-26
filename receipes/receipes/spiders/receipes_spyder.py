import scrapy

class ReceipesSpyder(scrapy.Spider):
    """ 
    This class scrapes desired urls. 
      
    Attributes: 
        real (int): The real part of complex number. 
        imag (int): The imaginary part of complex number. 
    """
    # define name of spyder
    name = "receipes"

    # define start urls
    start_ulrs = ["https://www.chefkoch.de/rezepte"]

    def parse(self, response):
        """
        Parse html reponse of scraper.

        Attributes:

        Returns:
            title (dict): Dict with title of receipe as value.
        """
        title = response.css("title").extract()

        yield {"title": title}