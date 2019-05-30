import subprocess

# not working yet
subprocess.call("scrapy", "crawl", "recipes", \
                    "-o", "items.json", \
                    "-s", "JSONDIR=crawls/recipes-1", \
                    "-t", "json", "2>", "some.text")