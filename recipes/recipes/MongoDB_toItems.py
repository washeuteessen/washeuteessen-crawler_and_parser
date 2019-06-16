import pymongo
import html2json
import json
import html

connMDB = pymongo.MongoClient('localhost',27017)
db = connMDB["test"]
collections = db["recipes"]
htmls = collections.find_one({"domain" : "chefkoch_html"})['htmlbody']
#print(json.dumps(htmls))