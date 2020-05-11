import requests
from config import *
import json
import pandas as pd
import datetime
def getNews(subject, startDate):
    feedback = requests.get(newsEndpoint,
    params={
        'q': subject,
        'sortBy': "popularity",
        'from': str(startDate),
        'to': str(startDate+datetime.timedelta(days=1)),
        'apiKey':newsApiKey,
    },
    headers={
        'Authorization':newsApiKey,
    } )
    print(feedback)
    print(startDate)
    print(startDate+datetime.timedelta(days=1))
    print(feedback.content)
    feedback = json.loads(feedback.content)
    feedback = feedback["articles"][:10]
    # print(json.dumps(feedback, indent=2))
    urls = []
    for i in range(len(feedback)):
        urls.append(feedback[i]["url"])

    # print(urls)
    return urls
    

date = datetime.datetime(2010,5,2)
print(date)
getNews("bitcoin", date)