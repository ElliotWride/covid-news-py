import requests
import json

def news_API_request(covid_terms = "Covid COVID_19 coronavirus", removed_articles = []):
    
    with open('config.json') as json_file:
        config = json.load(json_file)
    api_key = config['api_key']
    covid_terms = covid_terms.split() 
    query = ""
    for word in covid_terms:
        query = "q="+word+"&"+query
    url = ('https://newsapi.org/v2/everything?'
           +query+
           'sortBy=popularity&'
           'language = en&'
           'apiKey='+api_key)
    index = 0
    news_json = requests.get(url).json()['articles']
    
    if removed_articles != []:
        for article in news_json:
            for removed_article in removed_articles:
                if article == removed_article:
                    news_json.pop(index)
        
    return (news_json)


