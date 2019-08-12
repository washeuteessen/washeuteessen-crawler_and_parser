import time
from htmlParser import HTMLParser

# initialize parser
parser = HTMLParser()

# initialize number of recipes to skip
skip_recipes = 0

while True:
    # start parser
    check, skipped = parser.parse_html(skip_recipes=skip_recipes)
    
    # If last recipe was skipped, increase skip value by 1
    if skipped:
        skip_recipes = skip_recipes + 1

    # check if parser found unparsed doc
    if check == 0:
        
        # wait for 5 min (300 secs)
        time.sleep(300) 