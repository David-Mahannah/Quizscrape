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

# Crawls google search results
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

# Crawls quizlet.com decks
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
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)

def scrapeDaGoog(text):
    result_queue = Queue()
    crawler = CrawlerWorker(GoogSpider, result_queue, text)
    crawler.start()
    out = []
    for item in result_queue.get()[0]['link']:
        out.append(item.url)

    return out


def quizletScrape(text, url):
    result = Queue()
    crawler = QuizletWorker(QuizletSpider, result, text, url)
    crawler.start()
    out = []
    for card_holder in result.get():
        for i in card_holder['cards']:
            out.append(i)

    if len(out) > 0:
        return out
    else:
        return None;


class Cards:
    def __init__(self, question, result, resource, similarity):
        self.question = question
        self.result = result
        self.resource = resource
        self.similarity = similarity

    def __str__(self):
        return self.question + ":" + self.result

# Compares two strings by tokenizing them
def compareS(string1, string2):
    wnl = WordNetLemmatizer()
    lem_tok_1 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string1)]
    lem_tok_2 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string2)]
    c = [value for value in lem_tok_1 if value in lem_tok_2]
    return len(c) / max(len(lem_tok_1), len(lem_tok_2)) * 100


# Main method to run.
def run(text, minimum_similarity=60):
    # Collect links from scrapeDaGoog method
    google_links = scrapeDaGoog(text)
    
    # Run quizletScrape on each link in the deck
    out = []
    for link in google_links:
        # Since the links are unfiltered we need to select the ones that
        # are quizlet decks. 
        if "https://quizlet.com" in link:
            try:
                out.extend(quizletScrape(text, link.split("url?q=", 1)[1]))
    
    # Smash all the cards into a similarity algorithm and keep the
    # cards that are above the minimum_error
    matches = []
    for card in out:
        front = card['front']
        back = card['back']
        url = card['link']
        c1 = compareS(front, text)
        c2 = compareS(back, text)
        if (c1 > minimum_similarity):
            matches.append(Cards(front, back, url, round(c1, 2)))
        elif (c2 > minimum_similarity):
            matches.append(Cards(front, back, url, round(c2, 2)))

    # Bubble sort in ascending order of similarity
    n = len(matches)
    for i in range(n):
        for j in range(0, n-i-1):
            if matches[j].similarity < matches[j+1].similarity:
                matches[j], matches[j+1] = matches[j+1], matches[j]

    return matches


# Debug and Testing
if __name__ == '__main__':
    run("What is the capital of Germany?")