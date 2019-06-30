import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from recipes.spiders.chefkoch_spyder import ChefkochSpyder
from recipes.spiders.eatsmarter_spyder import EatsmarterSpyder
from recipes.spiders.essenundtrinken_spyder import EssenundtrinkenSpyder
#from recipes.spiders.ichkoche_spyder import IchkocheSpyder
from recipes.spiders.lecker_spyder import LeckerSpyder
from recipes.spiders.womenshealth_spyder import WomenshealthSpyder

# load project settings
setting = get_project_settings()

# define crawling process
process = CrawlerProcess(settings=settings)

# set spider name
spiderName = os.environ['SPIDER_NAME']

# start crawler
process.crawl(spiderName)
process.start()