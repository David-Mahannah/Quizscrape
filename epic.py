# Data structure used to store the results of the scrape
# Scrapy needs to return an Item object so this is the
# current solution

import scrapy

class Epic(scrapy.Item):
    link = scrapy.Field()
