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
            'mongo',
            27017
        )

        # load database
        self.db = conn["washeuteessen"]

        # load collections
        self.collection_raw = db["recipes_raw"]
        self.collection_view = db["unparsedURLS"]
        self.collection_parsed = db["recipes"]

        # set info if recipe was sucessfully parsed
        self.parsed = None

    def update_raw_recipes(parsed):
        """
        Method to store success of parsing in raw collection.
        """
        # write date and parsed status to mongo
        self.collection_raw.update(
            {"url": html["url"]},
            # write status and date to mongodb
            {"$set": {"parsed_status": parsed,
                      "$currentDate": {"parser_date": True}
                      }}                
        )

    def write_parsed_recipes(item):
        """
        Method to store extracted information into mongo DB.

        Returns:
        ------------
            Nothing, directly writes dict to Mongo DB.

        """
        logging.info(f"Write {item["url"]} to mongoDB...")

        # dump data to mongo DB
        self.collection_view.insert(dict(item))

    def parse_html():
        """
        Method to check domain of recipe and apply corresponding parsing method
        to extract relevant information from raw html.

        Returns:
        ------------
            item (dict): Json file with title, domain, image url, list of ingredients, url and text.
        """
        # randomly open 1x raw html
        html = self.collection_view.aggregate([{
            $sample: {size: 1}
        }])

        # create empty dict
        item = {}

        # get domain of raw html
        domain = html["domain"]

        logging.info(f"Parse {item["url"]} ...")

        # parse html
        if domain == "chefkoch":
            # get recipe title
            title = html["html_raw"].css(".page-title::text").extract_first()

            # get title picture
            img_src = html["html_raw"].css("a#0::attr(href)").extract_first()
            
            # get ingredients
            ingredients = html["html_raw"].xpath('//*[@id="recipe-incredients"]/div[1]/div[2]/table//tr')
            ingredients_list = []
            for ingredient in ingredients:
                # get name of ingredient
                if len(ingredient.xpath('td[2]//text()').extract_first().strip()) > 1:
                    ingredient = ingredient.xpath('td[2]//text()').extract_first().strip()
                else:
                    ingredient = ingredient.xpath('td[2]/a/text()').extract_first().strip()

                # append ingredient dict to ingredients list
                ingredients_list.append(ingredient)

            ingredients = ingredients_list

            # get text
            text = re.sub(" +", " ", " ".join(html["html_raw"].css("#rezept-zubereitung::text").extract()) \
                            .replace("\n", " ").replace("\r", " ")) \
                            .strip()

        elif domain == "eatsmarter":
            # get recipe title
            title = html["html_raw"].css("h1::text").extract_first()

            # get title picture
            img_src = html["html_raw"].css("img.photo::attr(src)").extract_first()

            # get ingredients
            ingredients = html["html_raw"].css('a.name::text').extract()

            # get text
            text = " ".join(html["html_raw"].css("div.preparation-step-items p::text").extract())

        elif domain == "lecker":
            # check if url contains a recipe
            if re.search(pattern="-[0-9]{5}.html$", string=html["url"]) is not None and re.search(pattern="datenschutzerklaerung", string=html["html_raw"].url) is None:

                # get recipe title
                title = html["html_raw"].css("h1::text").extract_first()
        
                # get title picture
                img_src = html["html_raw"].css(".article-figure--default-image img::attr(src)").extract_first()

                # version A of recipe presentation
                if img_src is not None:
                    # get ingredients
                    ingredients = html["html_raw"].css(".ingredientBlock::text").extract()

                    # get text
                    text = " ".join(html["html_raw"].css("dd::text").extract())
                    
                    # strip \n
                    text = re.sub("\n", "", text)

                    # strip whitespace
                    text = re.sub(" +", " ", text)
                    text = text.strip()

                # version B of recipe presentation 
                else:
                    # get url of main image
                    img_src = html["html_raw"].css(".typo--editor+ .article-figure--fullsize img::attrc(src)")

                    # get ingredients
                    ingredients = html["html_raw"].css("h2+ ul li::text").extract()

                    # get text
                    text = "no_distinct_text_available"

        elif domain == "essenundtrinken":
            # check if url contains a recipe
            if re.search(pattern="/rezepte/[0-9]{5}-", string=html["url"]) is not None and re.search(pattern=".jpg", string=html["html_raw"].url) is None:

                # get recipe title
                title = html["html_raw"].css(".headline-title::text").extract_first()
                title = title.strip()

                # get title picture
                img_src = html["html_raw"].css(".recipe-img > img:nth-child(1)::attr(src)").extract_first()

                # get ingredients
                ingredients = html["html_raw"].css("ul.ingredients-list li::text").extract()

                # strip \n
                ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

                # strip whitespace
                ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
                ingredients = [ingredient.strip() for ingredient in ingredients]

                # strip empty list elemens
                ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

                # get text
                text = " ".join(html["html_raw"].css("ul.preparation li.preparation-step div.preparation-text p::text").extract())

                # sometimes text is not within paragraph
                if len(text)<1:
                text = " ".join(html["html_raw"].css("ul.preparation li.preparation-step div.preparation-text::text").extract())

        elif domain == "womenshealth":
            # check if url contains a recipe
            if re.search(pattern="-rezept.[0-9]{7}.html", string=html["url"]) is not None:

                # get recipe title
                title = html["html_raw"].css(".v-A_-headline--ad::text").extract()[-1]
                title = title.strip()

                # get title picture
                img_src = html["html_raw"].css(".v-A_-article__hero__image > img:nth-child(1)::attr(src)").extract_first()

                # get ingredients
                ingredients = html["html_raw"].css("ul li::text").extract()

                # strip \n
                ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

                # strip whitespace
                ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
                ingredients = [ingredient.strip() for ingredient in ingredients]

                # strip empty list elemens
                ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

                # get text
                text = " ".join(html["html_raw"].css(".rdb-instructions li::text").extract())

        elif domain == "ichkoche":
        # TODO: 


        else:
            logging.info(f"No applicable parsing method found. 
                           Please check whether parsing scheme exists for desired {domain}.")
            self.parsed = 0

        # write found specs to item dict        
        if self.parsed = 0:
            logging.info(f"Skipping {html["url"]}")
    
        else:
            self.parsed = 1
            logging.info(f"Successfully parsed {html["url"]}")
            # store information as item
            item["title"] = title 
            item["domain"] = html["domain"]
            item["img_src"] = img_src
            item["ingredients"] = ingredients
            item["url"] = html["url"]
            item["text"] = text

            # write parsed recipe to mongo collection recipes
            write_parsed_recipes(item)

        update_raw_recipes(parsed)