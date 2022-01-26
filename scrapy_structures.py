# Data structure used to store the results of the scrape
# Scrapy needs to return an Item object so this is the
# current solution

import scrapy

class ScrapyLink(scrapy.Item):
    link = scrapy.Field()


class Card(scrapy.Item):
    front = scrapy.Field()
    back = scrapy.Field()
    link = scrapy.Field()


class CardHolder(scrapy.Item):
    cards = scrapy.Field()
