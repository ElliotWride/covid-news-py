# save this as app.py
from flask import Flask, render_template
from covid_data_handler import *
app = Flask(__name__)

@app.route('/')
def home():
   time_delay = 60
   
   last7day_cases, current_hospital_cases, total_deaths = schedule_covid_updates(time_delay,covid_api_request)
   
   return render_template('ECM1400 Flask Form Bootstrap Template.html', hospital_cases = current_hospital_cases, deaths_total= total_deaths, local_7day_infections = last7day_cases)

if __name__ == '__main__':
   app.run()
