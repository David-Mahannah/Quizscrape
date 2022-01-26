import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_structures import ScrapyLink

class GoogSpider(scrapy.Spider):
    def __init__(self, text):
        self.text = text

    def start_requests(self):
        urls = [
            "https://google.com/search?q={0} site:quizlet.com".format(self.text),
        ]

        for url in urls:
            #print("running url: ", url)
            yield scrapy.Request(url=url, callback=self.parse)

    name = "quotes"
    custom_settings = {
        'BOT_NAME' : 'quotes',
        'ROBOTSTXT_OBEY' : False
    }
    
    def parse(self, response):
        print("RESPONSE ", response)
        xlink = LinkExtractor()
        yield ScrapyLink(link=xlink.extract_links(response))

