from importlib.resources import path
from urllib import response
from flask import Flask
from pathlib import Path
import os
import random
import threading
import feedparser
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime



sys.path.insert(0, os.path.join(str(Path().absolute()), "urls"))

from news import NEWS


app = Flask(__name__)

newsIndex = {}
now = datetime.now()

def downloadNews(key, val):
    try:
        newsIndex[key] = []
        url = val
        blog=feedparser.parse(url)
        items= blog["entries"]
        for i in items:
            temp={}
            temp["title"]=i["title"]
            temp["link"]=i["link"]
            temp["pubDate"]=now.strftime("%d/%m/%Y")
            newsIndex[key].append(temp)
    except:
        print("error")


def getNews():
    for k, v in NEWS.items():
        threads = []
        for i in v:
            t = threading.Thread(target=downloadNews, args=(k, i))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        for i in v:
            downloadNews(k,i)
            
    print(newsIndex)



getNews()
sched = BackgroundScheduler(daemon=True)
sched.add_job(getNews, 'interval', minutes=30)
sched.start()


@app.route("/")
def home():
    response = {}
    response["top"] = newsIndex["top"]
    return response


@app.route('/<name>')
def category(name):
    response = {}
    response[name] = newsIndex[name]
    return response


if __name__ == '__main__':
    app.run(debug=True)
