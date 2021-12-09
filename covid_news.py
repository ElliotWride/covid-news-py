'''Accesses the covid API and returns relevent articles'''
import json
import requests

def news_API_request(covid_terms = "Covid COVID_19 coronavirus", removed_articles = []):
    '''Returns a json file of news articles using the news API and
    removes articles that have been previously cleared'''
    with open('config.json') as json_file:
        config = json.load(json_file)
    api_key = config['api_key']
    covid_terms = covid_terms.split()
    query = ""
    for word in covid_terms: #puts query together from inputted search terms
        query = "q="+word+"&"+query #becomes "&q=searchterm1&q=searchterm2"

    url = ('https://newsapi.org/v2/everything?'
           +query+
           'sortBy=popularity&'
           'language = en&'
           'apiKey='+api_key)
    news_json = requests.get(url).json()['articles'] #creates list of dictionaries of articles

    new_news_json = news_json.copy()
    if removed_articles: #if list of removed articles is not empty
        for article in news_json:
            for removed_article in removed_articles:
                if article == removed_article:
                    new_news_json.remove(article)

    return new_news_json
