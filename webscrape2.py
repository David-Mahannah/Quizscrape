# David Mahnnah
# mahannahd@gmail.com
# webscrape2.py
# The second iteration of my quizlet webscraper. Significant changes
# include:
# Transition from Selenium to BeautifulSoup for increased speeds
# New similarity algorithm implemented in compareS() that allows
# for a greater deal of diversity in results than the algorithms
# found in webscrape1.

import requests
import sys, getopt
import os
import csv
from bs4 import BeautifulSoup
from selenium  import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import time
from queue import Queue
import csv
import random
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log as urllibLogger
import concurrent.futures
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from proxy_finder import LoadUpProxies
from random import randrange
from webscrape3 import scrapeDaGoog

# This fixes multithreading lemmatizing
next(swn.all_senti_synsets())

# Object used to store the collected data from each quizlet card
class Card:
    def __init__(self, question, result, resource, similarity):
        self.question = question
        self.result = result
        self.resource = resource
        self.similarity = similarity

    def __str__(self):
        return self.question + ":" + self.results


class Webscrape2:
    def __init__(self, minimum_error=60):
        self.minimum_error = minimum_error

    def compareS(self, string1, string2):
        wnl = WordNetLemmatizer()
        lem_tok_1 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string1)]
        lem_tok_2 = [wnl.lemmatize(token) for token in nltk.word_tokenize(string2)]
        c = [value for value in lem_tok_1 if value in lem_tok_2]
        return len(c) / max(len(lem_tok_1), len(lem_tok_2)) * 100

    def GET_UA(self):
        uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
        ]
        return random.choice(uastrings)

    def searchQuizletDeck(self, link, text):
        headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}
        src = requests.get(link, headers=headers)
        soup = BeautifulSoup(src.content, "html.parser")
        #print(soup.prettify())
        cards = soup.find_all('div', class_="SetPageTerms-term")
        tidy = []
        for card in cards:
            front = card.find("span").encode_contents().decode('utf-8')
            back = card.find("span").find_next("span").encode_contents().decode('utf-8')
            tidy.append([front, back])

        matches = []
        for front, back in tidy:
            c1 = self.compareS(front, text)
            c2 = self.compareS(back, text)
            if (c1 > self.minimum_error):
                matches.append(Card(front, back, link, round(c1, 2)))
                # If found there probably isnt another
                break
            elif (c2 > self.minimum_error):
                matches.append(Card(front, back, link, round(c2, 2)))
                # If found there probably isnt another
                break
        return matches

    def quizletScrape(self, text):

        #s = requests.Session()
        # proxies = LoadUpProxies()
        # rnd=randrange(len(proxies))

        # randomIP=proxies[rnd]['ip']
        # randomPort=proxies[rnd]['port']
        # print(randomIP)
        # print(randomPort)

        # proxy_host = randomIP
        # proxy_port = randomPort

        # proxies = {
        #     "http": "http://53f21367c50e4569b807846ceabcab54:@proxy.crawlera.com:8010/"
        #     }
        
        #headers={'User-Agent': self.GET_UA()}
        # headers = {'User-Agent': self.GET_UA()}
        # print("Searching")
        # src = requests.get("https://google.com/search?q={0} site:Quizlet.com".format(text), proxies=proxies, verify="/home/david/Quizscrape/myprojectenv/lib/python3.8/site-packages/certifi/cacert.pem", headers=headers)
        # soup = BeautifulSoup(src.content, "html.parser")
        # print("Finished")
        # print(soup.prettify())
        # print("^ soup")
        # google_links = []
        # quizlet_links = []
        # divs = soup.find_all('div', class_="kCrYT")
        # for i in divs:
        #     link = i.find('a')
        #     if link:
        #         google_links.append(i.find('a').get('href'))

        # for link in google_links:
        #     if link.startswith("/url?q=https://quizlet.com/"):
        #         quizlet_links.append(link)
        # quizlet_links = ['/url?q=https://quizlet.com/40826338/germany-culture-questions-geography-flash-cards/', '/url?q=https://quizlet.com/109005066/german-border-countries-and-capitals-flash-cards/']
        quizlet_links = scrapeDaGoog(text)
        better_quizlet_links = []
        for link in quizlet_links:
            if "quizlet.com" in link.url: 
                better_quizlet_links = link.url
                print(better_quizlet_links)

        print("-------------------------")
        print(quizlet_links)
        # Split the links amoungst threads and collect the results in out
        # if the number of cards is 1 dont bother multithreading
        threads = []
        out = []
        if len(quizlet_links) > 1:
            with concurrent.futures.ThreadPoolExecutor() as executer:
                futures = [executer.submit(self.searchQuizletDeck, deck, text) for deck in better_quizlet_links]
                out = [f.result() for f in futures]

        else:
            out = []
            for thing in quizlet_links:
                out.append(searchQuizletDeck(thing[7:], text))

        outtest = []
        for k in out:
            if len(k) > 0:
                outtest.append(k[0])

    # Bubble sort the results
    # O(n^2). However, if we have only 7 cards the execution time is minimal
        n = len(outtest)
        for i in range(n):
            for j in range(0, n-i-1):
                if outtest[j].similarity < outtest[j+1].similarity :
                    outtest[j], outtest[j+1] = outtest[j+1], outtest[j]

        return outtest


# Testing Here
if __name__ == '__main__':
    str1 = "Direct method of learning about Earth's interior; taken by drilling holes or from explosions from volcanoes"
    str2 = "Direct method of learning about Earth's interior taken by mining holes or from explosions from eruptions"
    print(compareS(str1, str2))
