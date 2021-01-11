from scrapy import signals
from scrapy import settings
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher
from multiprocessing import Queue
import multiprocessing
from spider import GoogSpider

class CrawlerWorker(multiprocessing.Process):
    def __init__(self, spider, result_queue, text):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
        self.text = text
        self.crawler = CrawlerProcess()

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider, self.text)
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)

def scrapeDaGoog(text):
    result_queue = Queue()
    crawler = CrawlerWorker(GoogSpider, result_queue, text)
    crawler.start()
    out = []
    print(result_queue.get())
    for item in result_queue.get()[0]['link']:
        out.append(item.url)

    return out

if __name__ == '__main__':
    data =scrapeDaGoog("What is the capital of Germany?")
    print(len(data))
