from flask import Flask, render_template, request
from covid_data_handler import *
from covid_news import *
from datetime import datetime
import sched
import json
import threading

news_json = news_API_request()
news_json_removed = []
sched_updates_info = []
sched_updates_ui = []

scheduler = sched.scheduler(time.time, time.sleep)
with open('config.json') as json_file:
    config = json.load(json_file)
    
location = config['location']
location_type = config['location_type']
last7day_cases, current_hospital_cases, total_deaths = get_covid_data(location_type,location) #declaring global variables


def schedule_covid_data_updates(update_interval,update_name,location_type, location, repeat,time_completed):
    update = scheduler.enter(update_interval, 1, update_name, (location_type,location))
    sched_updates_info.append({"update":update,"time":time_completed,"repeat":repeat,"type":"data","name":update_name})
    t = threading.Thread(target=scheduler.run) #runs scheduler on different thread so the queue can be accessed by the program
    t.start()
    return (week_cases, hospital_cases, deaths)


def schedule_covid_news_updates(update_interval,update_name,news_json_removed, repeat, time_completed):
    update = scheduler.enter(update_interval, 2, update_name, ("Covid COVID_19 coronavirus",news_json_removed))
    sched_updates_info.append({"update":update,"time":time_completed,"repeat":repeat,"type":"news","name":update_name})
    t = threading.Thread(target=scheduler.run)
    t.start()
    news = news_json
    return news


def check_update_done(): #checks if update has reached its processing time
    time_now = datetime.strptime(datetime.strftime(datetime.now(),'%H:%M'),'%H:%M')
    index = 0
    for update in sched_updates_info:
        if update["time"] == time_now:
            if update["repeat"] == True: #schedules an identical update for 24hrs time if its a repeating update
                delay = sched_updates_info["time"] - time_now
                if update["type"] == "data":
                    schedule_covid_data_updates(delay,update["name"],location_type,location,update["repeat"],update["time"])
                else:
                    schedule_covid_news_updates(delay,update["name"],news_json_removed,update["repeat"],update["time"])
            else:                
                sched_updates_ui.pop(index)
                sched_updates_info.pop(index) #removes update
        index += 1
    
        
    
app = Flask(__name__)
@app.route('/index',methods=['GET', 'POST'])
def home():
   news = news_json
   
   if request.method == "GET":
      if request.args.get('notif'):
         index = 0
         for element in news:
            if element["title"] == request.args.get('notif'):
               news_json_removed.append(news_json.pop(index))
               break
            index +=1
            
      content = ""
      repeating, get_news, get_data = False, False, False
      if request.args.get('two'): #two is a query that is used when an update is called on the website, 
         delay = 0
         if request.args.get('repeat'):
            content += 'Repeated update, '
            repeating = True
         if request.args.get('covid-data'):
            content += 'Covid data update, '
            get_data = True
         if request.args.get('news'):
            content += 'News data update, '
            get_news = True
         if request.args.get('update'):
            content += 'Scheduled for - '+str(request.args.get('update')) #structures and gets all of the info of each update
            t1 = datetime.strptime(request.args.get('update'), '%H:%M')
            t2 = datetime.strptime(datetime.strftime(datetime.now(),'%H:%M'),'%H:%M')
            delay = (t1-t2).total_seconds()
        
         sched_updates_ui.append({"title":request.args.get('two'), "content":content}) #add schedule to website
         if get_data == True:
            schedule_covid_data_updates(delay,get_covid_data,location_type,location,repeating, t1)
         if get_news == True:
            news = schedule_covid_news_updates(delay,news_API_request,news_json_removed,repeating, t1)
         
      check_update_done()

      if request.args.get('update_item'): # remove from sched queue
         index = 0
         for update in sched_updates_ui:
            if update["title"] == request.args.get('update_item'):
               sched_updates_ui.pop(index)
               scheduler.cancel(sched_updates_info[index]["update"])
               break
            index +=1
      
      
         
      return render_template('index.html',location = location,nation_location = location_type, hospital_cases = current_hospital_cases,
                             deaths_total= total_deaths, local_7day_infections = last7day_cases,
                             news_articles = news, updates = sched_updates_ui, image = "covid.png")
      

   
   
   
     
   



if __name__ == '__main__':
   app.run()
