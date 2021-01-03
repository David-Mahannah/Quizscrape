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
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log as urllibLogger
import concurrent.futures

class Card:
    def __init__(self, question, result, resource, similarity):
        self.question = question
        self.result = result
        self.resource = resource
        self.similarity = similarity

text = "Which area is most likely to contain brackish water?"
LOGGER.setLevel(logging.NOTSET)
urllibLogger.setLevel(logging.NOTSET)
_sentinel = object()

def search_quizlet_deck(link, text, data_queue):
    chrome_options = Options()
    chrome_options.add_argument('--headless');
    chrome_options.add_argument('--disable-gpu');
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    cards = soup.find_all('div', class_="SetPageTerms-term")
    tidy = []
    for card in cards:
        front = card.find_all("span")[0].encode_contents().decode('utf-8')
        back = card.find_all("span")[1].encode_contents().decode('utf-8')
        tidy.append([front, back])

    print(tidy)
    minimum_error = 90
    matches = []
    found = false
    for front, back in tidy:
        c = front
        accuracy = 100
        length_of_original = float(len(c))
        if found:
            break
        while c != "":
            if accuracy < minimum_error:
                break
            elif (c in text):
                matches.append(Card(c, back, link, accuracy))
                found = true
                break
            else:
                c = c[0:len(c)-1]
                accuracy = (len(c) / length_of_original) * 100
    # n = len(matches)
    # for i in range(n):
    #     for j in range(0, n-i-1):
    #         if (matches[j].similarity > matches[j+1].similarity):
    #             matches[j], matches[j+1] = matches[j+1], matches[j]
    driver.quit()
    return matches

def quizletScrape(text):
    print(text)
    chrome_options = Options()
    chrome_options.add_argument('--headless');
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument('--disable-gpu');
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)

    # Format the name for a facebook url
    # Open link
    driver.get("https://google.com/search?q={0}".format(text))
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    results = soup.find_all("div", class_="g")
    # results = soup.find_all('h2', class_="result__title")
    links = []
    for i in results:
        links.append(i.find("a").get("href"))

    # Find all quizlet and wikipedia link
    quizlet_links = []
    wikepedia_links = []

    for link in links:
        if link.startswith("https://quizlet.com/"):
            quizlet_links.append(link)

        elif (link.startswith("https://en.wikipedia.org")):
            wikepedia_links.append(link)
        # else:
            #print("Not using " + link)

    # print("SIZEOFQUIZLETLINKS")
    # print(quizlet_links)
    #print(wikepedia_links)

    mega = []
    threads = []
    # Iterate over profile_cards and print names

    q = "bruh"

    with concurrent.futures.ThreadPoolExecutor() as executer:
        futures = [executer.submit(search_quizlet_deck, deck, text, q) for deck in quizlet_links]

    # print("THIS THIS HTIS SHHTISHTIHSITHISTISHIh")
    outtest = []
    out = [f.result() for f in futures]
    for k in out:
        if len(k) > 0:
            outtest.append(k[0])
    # print(outtest)
    return outtest

    # Close tab
    driver.quit()
