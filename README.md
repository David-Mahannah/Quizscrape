# Quizscrape - A search tool
A study in the risks of internet acesss in a education environment.

## Table of Contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Analysis](#Analysis)
* [Conclusion](#Conclusion)

## Introduction
Quizscrape is python webscraper for quiz answers using existing quizlet decks created by professors and students in the past.
With the COVID Pandemic bringing most schooling online, I noticed a much greater level of cheating amoungst my peers
through use of the web. Particularly in the form of searching through Quizlet decks. This project is an experiment 
to see to what extent the massive amount of public data online can be utilized for the purposes of academic dishonesty. Using Quizlet decks itself is not a new method of cheating but employing webscraping and automation greatily increases the harmfulness of this practice due to its far greater efficiency. I do not intend to use this personally and strongly suggest others not to use this in practice either for the sake of their own education. That being said, I did get a bit carried away with the ui design and presentation so just to be absolutely clear, **This application was made purely for the sake of experiment and not for personal use of monotization.** In fact, as I will refer to in my analysis, this tool proves of little use to a computer science student due to its behavior.

## Technologies
- Python
- Flask
- Beautiful Soup
- Selenium
- Scrapy

## Setup
### Virtual Environments

On Windows: `source myprojectenv\Scripts\activate.bat`

On Unix and Mac OS: `source myprojectenv/bin/activate`

To install requirements `pip install -r requirements.txt`
### Running the demo
After running:
`python app.py`
The demo can be found at: http://127.0.0.1:5000/ in your browser and should look as follows:

<img width="573" alt="Screen Shot 2022-01-25 at 9 27 50 AM" src="https://user-images.githubusercontent.com/44683761/151006616-eb857f2a-0bce-4f5e-a230-30e069ae6914.png">

## Analysis
### Use Cases
This tool is primarily effective at finding purely categorical data such as bio terms, or history dates. Essentially information that isnt highly dependent on the logically processing the questions provided. For example: the query: "What is the capital of France" likely exists as a flashcard while "What is 34 * 2 + 11" is unlikely to be on any flashcards. 
### Efficiency
Search times are highly dependent on the hardware that the code is run on. Particularly the processor as the program is utilizes multithreading. Faster machines will take around 5-10 seconds but slower machines could take anywhere from 30-60 seconds or longer. I'm certain more efficient approaches can be developed but this application is written as proof of concept rather than a fully functioning marketable application.

This project is far from perfect and may not run on all systems unless tinkered with a bit. The github branch history is a mess to say the least but served as a good tool to familiarize myself with github as both a tool for collaboration and project deployment. I am currently working to bring back the functionality of this code so a easily downloaded demo can be used. (1/25/22)
