import requests

url = ('https://newsapi.org/v2/everything?'
       'q=covid&'
       'from=2021-11-03&'
       'sortBy=popularity&'
       'apiKey=fda6003afe8840088037ff620156a1a9')
response = requests.get(url).json()
print (response)

url = ('https://newsapi.org/v2/everything?'
       'q=covid19&'
       'from=2021-11-03&'
       'sortBy=popularity&'
       'apiKey=fda6003afe8840088037ff620156a1a9')
response = requests.get(url).json()##can change .json to .csv
print (response)

##base for asking for news articles
