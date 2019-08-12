import re
import sys
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
import pymongo
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

## run mongo in docker
## open docker shell
# docker run -d -p 27017:27017 --name mongo mongo
# docker exec -it mongo /bin/sh
# mongo

class HTMLParser(object):
    """
    Class to get unparsed raw html source code and extract relevant recipe information.
    """

    def __init__(self):
        # connect to mongo
        self.conn = pymongo.MongoClient(
            "192.168.99.100", #'mongo',
            27017
        )

        # load database
        self.db = self.conn["recipes"]

        # load collections
        self.collection_raw = self.db["recipes_raw"]
        self.collection_parsed = self.db["recipes"]

        logging.info("Initialized parser")

    def update_raw_recipes(self, parsed, url):
        """
        Method to update raw collection with information about success and date.
        
        Returns:
        ------------
            Nothing, directly writes dict to Mongo DB collection_raw.
        """
        # write date and parsed status to mongo
        self.collection_raw.update(
            {"url": url},
            # write status and date to mongodb
            {"$set": {"parsed_status": parsed},
             "$currentDate": {"parser_date": True}
            }                
        )

    def write_parsed_recipes(self, item):
        """
        Method to store extracted information into mongo DB.

        Returns:
        ------------
            Nothing, directly writes dict to Mongo DB collection_view.

        """
        logging.info(f"Write {item['url']} to mongoDB...")

        # dump data to mongo DB
        self.collection_parsed.insert(dict(item))

    def parse_html(self):
        """
        Method to check domain of recipe and apply corresponding parsing method
        to extract relevant information from raw html.

        Returns:
        ------------
            item (dict): Json file with title, domain, image url, list of ingredients, url and text.
        """
        logging.info("Extracting unparsed sample from raw htmls")

        # randomly open 1x unaprsed raw html
        html = self.collection_raw.find_one({"parsed_status": False})

        # create empty dict
        item = {}

        # get domain of raw html
        domain = html["domain"]

        # convert raw html to html response object
        response = HtmlResponse(url=html["url"], body=html["html_raw"], encoding='utf-8')
        
        logging.info(f"Parse {html['url']} ...")
        
        # parse html
        if domain == "chefkoch":
            
            # get recipe title
            title = response.css("h1::text").extract_first()

            # get title picture
            img_src = response.css("meta[property='og:image']::attr(content)").extract_first()
            
            # get ingredients
            ingredients = response.css("td[class='td-right'] span::text").extract()

            # append ingredients saved as link text 
            ingredients.extend(response.css("td[class='td-right'] span a::text").extract())

            # strip whitespace from ingredients
            ingredients = [ingredient.strip() for ingredient in ingredients]

            # get text)
            text = re.sub(" +", " ", " ".join(response.xpath("/html/body/main/article[3]/div[1]/text()").extract()) \
                            .replace("\n", " ").replace("\r", " ")) \
                            .strip()
            
            # set parsed to True
            parsed = True

        elif domain == "eatsmarter":
            # get recipe title
            title = response.css("h1::text").extract_first()

            # get title picture
            img_src = response.css("img.photo::attr(src)").extract_first()

            # get ingredients
            ingredients = response.css('a.name::text').extract()

            # get text
            text = " ".join(response.css("div.preparation-step-items p::text").extract())
                
            # set parsed to True
            parsed = True

        elif domain == "lecker":
            # check if url contains a recipe
            if re.search(pattern="-[0-9]{5}.html$", string=html["url"]) is not None and re.search(pattern="datenschutzerklaerung", string=response.url) is None:

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

                        
            # set parsed to True
            parsed = True

        elif domain == "essenundtrinken":
            # check if url contains a recipe
            if re.search(pattern="/rezepte/[0-9]{5}-", string=html["url"]) is not None and re.search(pattern=".jpg", string=response.url) is None:

                # get recipe title
                title = response.css(".headline-title::text").extract_first()
                title = title.strip()

                # get title picture
                img_src = response.css(".recipe-img > img:nth-child(1)::attr(src)").extract_first()

                # get ingredients
                ingredients = response.css("ul.ingredients-list li::text").extract()

                # strip \n
                ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

                # strip whitespace
                ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
                ingredients = [ingredient.strip() for ingredient in ingredients]

                # strip empty list elemens
                ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

                # get text
                text = " ".join(response.css("ul.preparation li.preparation-step div.preparation-text p::text").extract())

                # sometimes text is not within paragraph
                if len(text)<1:
                    text = " ".join(response.css("ul.preparation li.preparation-step div.preparation-text::text").extract())
                        
            # set parsed to True
            parsed = True

        elif domain == "womenshealth":
            # check if url contains a recipe
            if re.search(pattern="-rezept.[0-9]{7}.html", string=html["url"]) is not None:

                # get recipe title
                title = response.css(".v-A_-headline--ad::text").extract()[-1]
                title = title.strip()

                # get title picture
                img_src = response.css(".v-A_-article__hero__image > img:nth-child(1)::attr(src)").extract_first()

                # get ingredients
                ingredients = response.css("ul li::text").extract()

                # strip \n
                ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

                # strip whitespace
                ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
                ingredients = [ingredient.strip() for ingredient in ingredients]

                # strip empty list elemens
                ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

                # get text
                text = " ".join(response.css(".rdb-instructions li::text").extract())
                        
            # set parsed to True
            parsed = True

        elif domain == "ichkoche":
            # get recipe title
            title = response.xpath("//title/text()").extract_first()[:-28]

            # get title picture
            img_src = response.xpath("//img[@itemprop='image']/@src").extract_first()
            #//*[@id="page_wrap_inner"]/div[3]/div/div[2]/article[1]

            ## get ingredients
            # extract ingredients which contain links
            ingredients_a = response.xpath("//div[@class='ingredients_wrap']/ul/li/span/a/text()").extract()

            # extract links which don't contain links
            ingredients_b = response.xpath("//div[@class='ingredients_wrap']/ul/li/span[@class='name']/text()").extract()

            # combine both lists
            ingredients_list = ingredients_a + ingredients_b
            ingredients = ingredients_list

            # get text
            texts_list = response.xpath("//div[@class='description']/ol/li").extract()
            text = " ".join([re.sub("<br>|<li>|<strong>|</strong>|</li>", " ", text).strip() for text in texts_list])

            # set parsed to True
            parsed = True

        else:
            logging.info(f"No applicable parsing method found. Please check whether parsing scheme exists for desired {domain}.")
            parsed = False

        # write found specs to item dict        
        if parsed == False:
            logging.info(f"Skipping {html['url']}")
    
        else:
            parsed = True
            logging.info(f"Successfully parsed {html['url']}")
            # store information as item
            item["title"] = title 
            item["domain"] = html["domain"]
            item["img_src"] = img_src
            item["ingredients"] = ingredients
            item["url"] = html["url"]
            item["text"] = text

            # write parsed recipe to mongo collection recipes
            self.write_parsed_recipes(item)

        self.update_raw_recipes(parsed, html["url"])

if __name__ == "__main__":
    parser = HTMLParser()
    parser.parse_html()