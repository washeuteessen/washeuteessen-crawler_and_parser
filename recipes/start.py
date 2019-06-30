from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from recipes.spiders.chefkoch_spyder import ChefkochSpyder

process = CrawlerProcess(get_project_settings())
process.crawl(ChefkochSpyder)
process.start()
