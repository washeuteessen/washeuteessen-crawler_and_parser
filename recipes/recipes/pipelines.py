# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class RecipesPipeline(object):
    def __init__ (self):
        
        # Connecting to Server with Name and Port
        self.conn = pymongo.MongoClient(
            '192.168.99.100', #VM IP-address
            '127.0.0.1'
            27017
        )
        
        # Choosing Database and Collection
        db = self.conn["washeuteessen"]
        self.collection = db["recipes_html_raw"]

    def process_item(self, item, spider):
        
        # Inserting Scraped item into MongoDB
        self.collection.insert(dict(item))

        return item