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
    # define the fields for your item here like:
    title = scrapy.Field()
    domain = scrapy.Field()
    img_src = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    ingredients = scrapy.Field()

class RecipesHtml(scrapy.Item):
    htmlbody = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()