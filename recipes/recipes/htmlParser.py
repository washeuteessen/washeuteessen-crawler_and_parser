import logging
import pymongo

## run mongo in docker
## open docker shell
# docker run -d -p 27017:27017 --name mongo mongo
# docker exec -it mongo /bin/sh
# mongo

class HTMLParser(object):
    def __init__(db_name, col_name):
        # connect to mongo
        self.conn = pymongo.MongoClient(
            '192.168.99.100', #VM IP-address
            27017
        )

        # load database
        self.db = conn["washeuteessen"]

        # load collections
        self.collection_view = db["_recipes_view"]
        self.collection_parsed = db["recipes_parsed"]

    def parse_html():
        """
        Method to check domain of recipe and apply corresponding parsing method
        to extract relevant information from raw html.

        Returns:
        ------------
            item (dict): Json file with title, domain, image url, list of ingredients, url and text.
        """
        # open raw html
        html = self.collection.find()

        # create empty dict
        item = {}

        # get domain of raw html
        domain = html["domain"]

        # parse html
        if domain == "chefkoch":
            # get recipe title
            title = response.css(".page-title::text").extract_first()

            # get title picture
            img_src = response.css("a#0::attr(href)").extract_first()
            
            # get ingredients
            ingredients = response.xpath('//*[@id="recipe-incredients"]/div[1]/div[2]/table//tr')
            ingredients_list = []
            for ingredient in ingredients:
                # get name of ingredient
                if len(ingredient.xpath('td[2]//text()').extract_first().strip()) > 1:
                    ingredient = ingredient.xpath('td[2]//text()').extract_first().strip()
                else:
                    ingredient = ingredient.xpath('td[2]/a/text()').extract_first().strip()

                # append ingredient dict to ingredients list
                ingredients_list.append(ingredient)

            # get text
            text = re.sub(" +", " ", " ".join(response.css("#rezept-zubereitung::text").extract()) \
                            .replace("\n", " ").replace("\r", " ")) \
                            .strip()

        elif domain == "eatsmarter":
            pass

        elif domain == "lecker":
            pass

        elif domain == "essenundtrinken":
            pass

        elif domain == "womenshealth":
            pass

        else:
            logging.info(f"No applicable parsing method found. Please check whether parsing scheme exists for desired {domain}.")
    
        # store information as item
        item["title"] = title 
        item["domain"] = domain
        item["img_src"] = img_src
        item["ingredients"] = ingredients_list
        item["url"] = html["url"]
        item["text"] = text

        return item

    def write_to_mongo(item):
        """
        Method to store extracted information into mongo DB.

        Returns:
        ------------
            Nothing, directly writes dict to Mongo DB.

        """
        # dump data to mongo DB
        self.collection.insert(dict(item))