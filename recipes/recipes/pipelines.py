# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class RecipesPipeline(object):
    # Initialise of the class
    def __init__(self):
        # Connecting to Server with Name and Port
        self.conn = pymongo.MongoClient(
            'mongo',
            27017
        )

        # Choosing Database and Collection
        db = self.conn["recipes"]
        self.collection = db["recipes"]

    # Processing
    def process_item(self, item, spider):
        """
        Function to insert scraped item into MongoDB
        """
        
        # Convert item to dict
        item_dict = dict(item)
        
        # Trying to update existing document with htmlbody and current time
        documentupdated = self.collection.update({"url": item_dict["url"]},
                                                 {"$set":{"title":item_dict["title"],
                                                          "ingredients":item_dict["ingredients"],
                                                          "text":item_dict["text"],
                                                          "img_src":item_dict["img_src"]},
                                                  "$currentDate": {"lastFound": True}
                                                  }
                                                )
        
        # If update Failed insert new document
        if documentupdated["matchedCount"] == 0:
            self.collection.insert(item_dict)
        
        return item