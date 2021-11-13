# save this as app.py
from flask import Flask, render_template, request
from covid_data_handler import *
from newsAPI import *
app = Flask(__name__)

testDict = {
   "title" : ["1","2","3","4","5","6","7","8"]
   }


@app.route('/index',methods=['GET', 'POST'])
def home():
   time_delay = 60
   allNews = response
   articles = allNews["articles"]
   last7day_cases, current_hospital_cases, total_deaths = schedule_covid_updates(time_delay,covid_api_request)


   if request.method == "POST":
      print("post")
   
   elif request.method == "GET":
      print(request.args.get('notif'))
      if request.args.get('notif'):
         print("test")
         index = 0
         for element in articles:
            if element["title"] == request.args.get('notif'):
               articles.pop(index)
            index +=1
   
      
   return render_template('index.html', hospital_cases = current_hospital_cases,
                          deaths_total= total_deaths, local_7day_infections = last7day_cases,
                          news_articles = articles)



if __name__ == '__main__':
   app.run()
