#!/usr/bin/python

from flask import Flask, request
from weather import weather
from stocks import stocks
from htmlparser import htmlparser
from rss import rss


app = Flask(__name__)

@app.route('/')
def getIndexHtml():
    with open('static/index.html', 'r') as indexhtml:
        return indexhtml.read()

app.register_blueprint(weather)
app.register_blueprint(stocks)
app.register_blueprint(htmlparser)
app.register_blueprint(rss)










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
