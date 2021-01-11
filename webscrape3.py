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
        print("LOG: starting :GOL")
        self.crawler.start()
        print("LOG: stopping :GOL")
        self.crawler.stop()
        print("LOG: putting in queue :GOL")
        self.result_queue.put(self.items)
        print("LOG: done :GOL")

def scrapeDaGoog(text):
    result_queue = Queue()
    crawler = CrawlerWorker(GoogSpider, result_queue, text)
    crawler.start()
    #crawler.stop()
    print("Alive? ", crawler.is_alive())
    out = []
    print(result_queue.get())
    print("CHECKPOINT 1")
    for item in result_queue.get()[0]['link'][:8]:
        print("yeet", item)
        out.append(item.url)

    print("CHECKPOINT 2")
    crawler.stop()
    print("CHECKPOINT 3")
    crawler.terminate()
    return out

#if __name__ == '__main__':
    #data =scrapeDaGoog("What is the capital of Germany?")
    #print(len(data))
