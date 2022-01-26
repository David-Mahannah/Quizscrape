import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_structures import Card, CardHolder

class QuizletSpider(scrapy.Spider):
    def __init__(self, text, urls):
        self.text = text
        self.urls = urls

    def start_requests(self):
        urls = [
            self.urls
        ]

        for url in urls:
            print("Crawling url: ", url)
            yield scrapy.Request(url=url, callback=self.parse)

    name = "quizlet_scraper"
    custom_settings = {
            'DOWNLOADER_MIDDLEWARES' : {
                "scrapy_crawlera.CrawleraMiddleware": 610,
            },
            'CRAWLERA_ENABLED' : True,
            'CRAWLERA_APIKEY' : '53f21367c50e4569b807846ceabcab54',
            #'LOG_FORMATTER' : 'crawlera_fetch.CrawleraFetchLogFormatter',
            'BOT_NAME' : 'quizlet_scraper',
            'ROBOTSTXT_OBEY' : False
    }
    def parse(self, response):
        #print("parsing")
        #print(response)
        #print(response.css('title'))
        #xlink = LinkExtractor()
        #print(len(response.xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div/div[1]/section/div').getall()))
        cards = response.xpath("//div[@class='SetPageTerms-term']")
        #print(cards)
        out = CardHolder(cards=[])
        for card in cards:
            c = card.xpath('.//span/text()').getall()
            front = c[0]
            back = c[1]
            #print(front)
            #print(back)
            out['cards'].append(Card(front=front, back=back, link=self.urls))
            #front = card.xpath('//span[contains(@class, "TermText")]').get()
            #back = card.xpath('//span[contains(@class, "Termtext")]').get()
            #print(front)
            #print(back)
            #print(card)

        #front = response.css("div.SetPageTerm-content div.SetPageTerm-smallSide div.SetPageTerm-sideContent a.SetPageTerm-wordText").get()
        #back = response.css("div.SetPageTerm-content div.SetPageTerm-largeSide div.SetPageTerm-sideContent a.SetPageTerm-wordText").get()
        return out
