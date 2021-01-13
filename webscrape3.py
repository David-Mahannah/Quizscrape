from scrapy import signals
from scrapy import settings
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher
from multiprocessing import Queue
import multiprocessing
from spider import GoogSpider
from spider2 import QuizletSpider
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

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

class QuizletWorker(multiprocessing.Process):
    def __init__(self, spider, result_queue, text, url):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
        self.text = text
        self.url = url
        self.crawler = CrawlerProcess()

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider, self.text, self.url)
        print("LOG: starting :GOL")
        self.crawler.start()
        print("LOG: stopping :GOL")
        self.crawler.stop()
        print("LOG: putting in queue GOL")
        self.result_queue.put(self.items)
        print("LOG: done :GOL")

def scrapeDaGoog(text):
    result_queue = Queue()
    crawler = CrawlerWorker(GoogSpider, result_queue, text)
    crawler.start()
    #crawler.stop()
    #print("Alive? ", crawler.is_alive())
    #print("---------------------------")
    out = []
    #print(result_queue.get())
    #print("CHECKPOINT 1")
    #print(result_queue.get())
    #return result_queue.get()[0]['link'][:8]
    for item in result_queue.get()[0]['link']:
        print("Hellow")
        #yield item
    #    print(item.url)
        out.append(item.url)

    #print("CHECKPOINT 2")
    #crawler.stop()
    #print("CHECKPOINT 3")
    # crawler.terminate()
    return out


def quizletScrape(text, url):
    result = Queue()
    crawler = QuizletWorker(QuizletSpider, result, text, url)
    print("oy")
    crawler.start()
    #print("yey")

    out = []
    #print(len(result.get()))
    for card_holder in result.get():
        print("----------")
        for i in card_holder['cards']:
            out.append(i)
            print(i['front'], i['back'])
        #print(card.back)
        #print("----------")
    
    #print("we out here")
    if len(out) > 0:
        print("Found something")
        return out
    else:
        print("Nothing found")
        return None;


class Cards:
    def __init__(self, question, result, resource, similarity):
        self.question = question
        self.result = result
        self.resource = resource
        self.similarity = similarity

    def __str__(self):
        return self.question + ":" + self.result


def compareS(string1, string2):
    wnl = WordNetLemmatizer()
    lem_tok_1 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string1)]
    lem_tok_2 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string2)]
    c = [value for value in lem_tok_1 if value in lem_tok_2]
    return len(c) / max(len(lem_tok_1), len(lem_tok_2)) * 100


#if __name__ == '__main__':
def run(text):
    #print("=====================================================================================")
    data = scrapeDaGoog(text)
    print(data)
    counter = 1
    out = []
    for link in data:
        if "https://quizlet.com" in link:
            print("ITERATION ", counter)
            out.extend(quizletScrape(text, link.split("url?q=", 1)[1]))
            counter = counter + 1
    
    print(out)

    minimum_error = 60
    
    matches = []
    for card in out:
        front = card['front']
        back = card['back']
        url = card['link']

        c1 = compareS(front, text)
        c2 = compareS(back, text)
        if (c1 > minimum_error):
            matches.append(Cards(front, back, url, round(c1, 2)))
        elif (c2 > minimum_error):
            matches.append(Cards(front, back, url, round(c2, 2)))
   
    #for card in matches:
    #    print(card.question, card.result, card.similarity, card.resource)

    n = len(matches)
        for i in range(n):
            for j in range(0, n-i-1):
                if matches[j].similarity < matches[j+1].similarity :
                    matches[j], matches[j+1] = matches[j+1], matches[j]


    return matches
    #print(matches)
    #print(out)



if __name__ == '__main__':
    run("What is the capital of Germany?")
