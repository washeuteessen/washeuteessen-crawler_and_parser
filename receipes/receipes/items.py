# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReceipesItem(scrapy.Item):
    """
    Stores the extracted data as scrapy item.
    """
    # define the fields for your item here like:
    title = scrapy.Field()
    img_src = scrapy.Field()
    url = scrapy.Field()