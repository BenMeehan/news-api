from urllib import response
from flask import Flask
from pathlib import Path
import os
import requests
import threading
import sys
from apscheduler.schedulers.background import BackgroundScheduler


sys.path.insert(0,os.path.join(str(Path().absolute()),"urls"))

from news import NEWS


app = Flask(__name__)

newsIndex={}

def downloadNews(key,val):
    newsIndex[key]=[]
    url=val
    response = requests.get(url)
    # Further processing
    newsIndex[key]+=response.json()['items']


def getNews():
    for k,v in NEWS.items():
        threads=[]
        for i in v:
            t=threading.Thread(target=downloadNews,args=(k,i))
            threads.append(t)
    
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
    
    print("To database")
    

getNews()   
sched = BackgroundScheduler(daemon=True)
sched.add_job(getNews,'interval',minutes=30)
sched.start()

@app.route("/")
def home():
    response={}
    response["top"]=newsIndex["top"]   
    return response     

@app.route('/<name>')
def hello_world(name):
    response={}      
    response[name]=newsIndex[name]
    return response

if __name__ == '__main__':
   app.run(debug=True)