from datetime import date
from uk_covid19 import Cov19API
from datetime import date
import time
import sched
scheduler = sched.scheduler(time.time, time.sleep)
cases_and_deaths = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType" : "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
    "hospitalCases" : "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate" 
}


def schedule_covid_updates(update_interval,update_name):
    print("updating...")
    update_name("nation","England")
    csv_data = parse_csv_data("nation_"+str(date.today())+".csv")
    last7day_cases, current_hospital_cases, total_deaths = process_covid_csv_data(csv_data)
    scheduler.enter(update_interval, 1,schedule_covid_updates, (update_interval, update_name))
    scheduler.run(blocking = False)
    return (last7day_cases, current_hospital_cases, total_deaths)


def covid_api_request(location_type = "ltla", location = "Exeter"):
    
    location_filter = ["areaType="+location_type,"areaName="+location]
    api = Cov19API(filters=location_filter, structure=cases_and_deaths)
    data = api.get_csv()
    with open("nation_"+str(date.today())+".csv", "w") as myfile:
        myfile.write(data)
        
    lines = parse_csv_data("nation_"+str(date.today())+".csv")

    last7day_cases, current_hospital_cases, total_deaths = process_covid_csv_data(lines)
    print(last7day_cases, current_hospital_cases, total_deaths)

def parse_csv_data(csv_file_name):
    with open(csv_file_name) as file:
        lines = file.readlines()
    return lines


def process_covid_csv_data(covid_csv_data):
    last7day_cases = 0
    total_deaths = 0
    current_hospital_cases = 0    
    for i in range (1,8):
        if (covid_csv_data[i].split(",")[6] != "\n"):
            last7day_cases += int(covid_csv_data[i].split(",")[6])
    current_hospital_cases = covid_csv_data[2].split(",")[5]
    for i in range (1,len(covid_csv_data)):
        if covid_csv_data[i].split(",")[4] != "":
            total_deaths = covid_csv_data[i].split(",")[4]
            break
    return last7day_cases, current_hospital_cases, total_deaths
        

        

def main():
    time_delay = 5
    schedule_covid_updates(time_delay,covid_api_request)    
   

if __name__ == "__main__":
    main()

    

