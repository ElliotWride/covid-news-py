import requests
import json

def news_API_request(covid_terms = "Covid COVID_19 coronavirus"):
    with open('config.json') as json_file:
        config = json.load(json_file)
    api_key = config['api_key']
    covid_terms = covid_terms.split() 
    query = ""
    for word in covid_terms:
        query = "q="+word+"&"+query
    url = ('https://newsapi.org/v2/top-headlines?'
           +query+
           'sortBy=popularity&'
           'language = en&'
           'apiKey='+api_key)
    return (requests.get(url).json())

