import pymongo
import html2json
import json
import html

# run mongo in docker
# open docker shell
# docker exec -it mongo /bin/sh
# mongo

class HTMLParser(object):
    def __init__(db_name, col_name):
        # connect to mongo
        self.connMDB = pymongo.MongoClient('localhost',27017)

        # get database and collection
        self.db = connMDB["washeuteessen"]
        self.collection = db["recipes"]

    def parse_html():
        # open raw html
        htmls = self.collection.find_all()

        # iterate over htmls
        for html in htmls:

            # get domain of raw html
            domain = html["domain"]

            # parse html
            if domain == "chefkoch":
            else domain == ""

