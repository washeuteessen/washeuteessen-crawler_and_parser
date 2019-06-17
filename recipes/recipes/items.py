# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
    """
    Stores the extracted data as scrapy item.
    """
    # define the fields (dict keys) for item
    htmlbody = scrapy.Field()
    domain = scrapy.Field()