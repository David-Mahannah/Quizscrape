
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from csv import reader
from webscrape2 import Webscrape2
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# Flask constructor takes the name of
# current module (__name__) as argument.

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
scraper = Webscrape2()

app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

db = SQLAlchemy(app)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_results = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.String(120), nullable=False)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/news')
def news():
    return render_template('newsletter.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit_search', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        r = request.form['q']
        start_time = time.time()
        #list_of_rows = scrapeDaGoog(r)
        #print(type(list_of_rows))
        list_of_rows = scraper.quizletScrape(r)
        print("--- %s seconds ---" % (time.time() - start_time))
        #db.session.add(Search(number_of_results=len(list_of_rows), time=time.time() - start_time))
        #db.session.commit()
        #db.session.add(Search(number_of_results=len(list_of_rows), time=time.time() - start_time))

        # time.sleep(15)
        # with open ('data.csv', 'r') as read_obj:
        #     csv_reader = reader(read_obj)
        #     list_of_rows = list(csv_reader)
        #
        # print("++++++++++++")
        # print(list_of_rows)
        return render_template('results.html', results=list_of_rows, question=r)
    else:
        return "Bruh"



# main driver function
# if __name__ == '__main__':
#     app.run()
