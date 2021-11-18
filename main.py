from flask import Flask, render_template, request
from covid_data_handler import *
from covid_news import *
from datetime import datetime
import sched
import json
news_json = news_API_request()
sched_updates_id = []
sched_updates_ui = []
scheduler = sched.scheduler(time.time, time.sleep)

with open('config.json') as json_file:
    config = json.load(json_file)
location = config['location']
location_type = config['location_type']
last7day_cases, current_hospital_cases, total_deaths = get_covid_data(location_type,location)
articles = news_json["articles"]


def schedule_covid_updates(update_interval,update_name):
    update = scheduler.enter(update_interval, 1, update_name, ())
    sched_updates_id.append(list(update))
    #print(sched_updates_id)
    #print(scheduler.queue)
    scheduler.run()
    return (week_cases, hospital_cases, deaths)

app = Flask(__name__)
@app.route('/index',methods=['GET', 'POST'])



def home():
   
   
   if request.method == "POST":
      print("post")
      
         
   
   elif request.method == "GET":
      if request.args.get('notif'):
         index = 0
         for element in articles:
            if element["title"] == request.args.get('notif'):
               articles.pop(index)
               break
            index +=1
      content = ""
      repeat, get_news, get_data = False, False, False
      if request.args.get('two'):
         if request.args.get('repeat'):
            content += 'Repeated update, '
            repeat = True
         if request.args.get('covid-data'):
            content += 'Covid data update, '
            get_data = True
         if request.args.get('news'):
            content += 'News data update, '
            get_news = True
         if request.args.get('update'):
            content += 'Scheduled for - '+str(request.args.get('update'))
            t1 = datetime.strptime(request.args.get('update'), '%H:%M')
            t2 = datetime.strptime(datetime.strftime(datetime.now(),'%H:%M'),'%H:%M')
            delay = (t1-t2).total_seconds()
                   
         else:
            sched_json.append({"title":request.args.get('two'), "delay":0})
            delay = 0
         sched_updates_ui.append({"title":request.args.get('two'), "content":content})
         if get_data == True:
            schedule_covid_updates(delay,get_covid_data,location_type,location)
         if get_news == True:
            schedule_covid_updates(delay,news_API_request)


      if request.args.get('update_item'):
         index = 0
         for update in sched_updates_ui:
            if update["title"] == request.args.get('update_item'):
               sched_updates_ui.pop(index)
               print(sched_updates_id[index])
               scheduler.cancel(sched_updates_id[index])

               break
            index +=1

      
         
      return render_template('index.html', hospital_cases = current_hospital_cases,
                             deaths_total= total_deaths, local_7day_infections = last7day_cases,
                             news_articles = articles, updates = sched_updates_ui)
      

   
   
   
     
   



if __name__ == '__main__':
   app.run()
