'''Interacts with the webpage, manages sheduling of updates, handles user requests and passes data to the website'''
import sched
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request
from covid_data_handler import get_covid_data
from covid_news import news_API_request

news_json = news_API_request()
news_json_removed = []
sched_updates_info = []
sched_updates_ui = []

scheduler = sched.scheduler(time.time, time.sleep)
with open('config.json') as json_file:
    config = json.load(json_file)

NEWS_TERMS = config["news_terms"]
LOCATION = config['location']
LOCATION_TYPE = config['location_type']
NATION = config['nation']
NATIONAL_LAST7DAY_CASES, LOCAL_LAST7DAY_CASES, CURRENT_HOSPITAL_CASES, TOTAL_DEATHS = get_covid_data(LOCATION_TYPE,LOCATION,NATION)

def schedule_covid_data_updates(update_interval, update_name, LOCATION_TYPE, LOCATION, repeat, time_completed, NATION):
    '''Adds a covid data update to the queue'''
    update = scheduler.enter(update_interval, 1, update_name, (LOCATION_TYPE,LOCATION, NATION))
    sched_updates_info.append({"update":update,"time":time_completed,"repeat":repeat,"type":"data","name":update_name})
    thread = threading.Thread(target=scheduler.run) #runs scheduler on different thread so the queue can be accessed by the program
    thread.start()
    return (NATIONAL_LAST7DAY_CASES, LOCAL_LAST7DAY_CASES, CURRENT_HOSPITAL_CASES, TOTAL_DEATHS)


def schedule_covid_news_updates(update_interval,update_name,news_json_removed, repeat, time_completed):
    '''Adds a news update to the queue'''
    update = scheduler.enter(update_interval, 2, update_name, (NEWS_TERMS,news_json_removed))
    sched_updates_info.append({"update":update,"time":time_completed,"repeat":repeat,"type":"news","name":update_name})
    thread = threading.Thread(target=scheduler.run)
    thread.start()
    news = news_json
    return news


def check_update_done(): #checks if update has reached its processing time
    '''Checks the current time against the time of due updates then deletes or queues an identical update for the next day'''
    time_now = datetime.strptime(datetime.strftime(datetime.now(),'%H:%M'),'%H:%M')
    index = 0
    for update in sched_updates_info:
        if update["time"] == time_now:
            if update["repeat"] is True: #schedules an identical update for 24hrs time if its a repeating update
                delay = sched_updates_info["time"] - time_now
                if update["type"] == "data":
                    schedule_covid_data_updates(delay,update["name"],LOCATION_TYPE,LOCATION,update["repeat"],update["time"])
                else:
                    schedule_covid_news_updates(delay,update["name"],news_json_removed,update["repeat"],update["time"])
            else:
                sched_updates_ui.pop(index)
                sched_updates_info.pop(index) #removes update
        index += 1



app = Flask(__name__)
@app.route('/index',methods=['GET', 'POST'])
def home():
    '''Interacts with the webpage, processes all actions taken on the site and passes data to the webpage'''
    news = news_json
    global NATIONAL_LAST7DAY_CASES, LOCAL_LAST7DAY_CASES, CURRENT_HOSPITAL_CASES, TOTAL_DEATHS
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
        if request.args.get('two'): #two is a query that is used when an update is called on the website
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
                time_update = datetime.strptime(request.args.get('update'), '%H:%M')
                time_now = datetime.strptime(datetime.strftime(datetime.now(),'%H:%M'),'%H:%M')
                delay = (time_update-time_now).total_seconds()
            if get_data is True or get_news is True: #only creates an update if data or news is selected
                if delay == 0:
                    if get_data is True:
                        NATIONAL_LAST7DAY_CASES, LOCAL_LAST7DAY_CASES, CURRENT_HOSPITAL_CASES, TOTAL_DEATHS = get_covid_data(LOCATION_TYPE,LOCATION,NATION)
                    if get_news is True:
                        news = news_API_request(NEWS_TERMS,news_json_removed)
                else:
                    sched_updates_ui.append({"title":request.args.get('two'), "content":content}) #add schedule to website
                    if get_data is True:
                        NATIONAL_LAST7DAY_CASES, LOCAL_LAST7DAY_CASES, CURRENT_HOSPITAL_CASES, TOTAL_DEATHS = schedule_covid_data_updates(delay,get_covid_data,LOCATION_TYPE,LOCATION,repeating, time_update, NATION)
                    if get_news is True:
                        news = schedule_covid_news_updates(delay, news_API_request, news_json_removed, repeating, time_update)

        check_update_done()

        if request.args.get('update_item'): # remove from sched queue
            index = 0
            for update in sched_updates_ui:
                if update["title"] == request.args.get('update_item'):
                    sched_updates_ui.pop(index)
                    scheduler.cancel(sched_updates_info[index]["update"])
                    sched_updates_info.pop(index)
                    break
                index +=1


    return render_template('index.html',
                           location = LOCATION,nation_location = NATION,
                           hospital_cases = "Current hospital cases: " + str(CURRENT_HOSPITAL_CASES),
                           deaths_total= "Total deaths: "+str(TOTAL_DEATHS),
                           local_7day_infections = LOCAL_LAST7DAY_CASES,
                           national_7day_infections = NATIONAL_LAST7DAY_CASES,
                           news_articles = news, updates = sched_updates_ui,
                           image = "covid.png")


if __name__ == '__main__':
    app.run()
