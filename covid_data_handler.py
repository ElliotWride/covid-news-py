from datetime import date
from uk_covid19 import Cov19API
from datetime import date
import time



week_cases = 0
hospital_cases = 0
deaths = 0

cases_and_deaths = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType" : "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
    "hospitalCases" : "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate" 
}


def covid_api_request(location_type = "ltla", location = "Exeter"):
    location_filter = ["areaType="+location_type,"areaName="+location]
    api = Cov19API(filters=location_filter, structure=cases_and_deaths)
    data = api.get_json()
    return data


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
        
def get_covid_data(location_type= "ltla",location = "Exeter"):
    data = covid_api_request(location_type,location)
    for dic in data["data"]:
        if dic["cumDailyNsoDeathsByDeathDate"] !=None:
            total_deaths = dic["cumDailyNsoDeathsByDeathDate"]
            break

    for dic in data["data"]:
        if dic["hospitalCases"] !=None:
            current_hospital_cases = dic["hospitalCases"]
            break
    
        
    days = 0
    last7day_cases = 0
    for dic in data["data"]:
        if dic["newCasesBySpecimenDate"] != None:
            days +=1
            last7day_cases += dic["newCasesBySpecimenDate"]            
        if days == 7:
            break
    global week_cases, hospital_cases, deaths
    week_cases, hospital_cases, deaths = last7day_cases, current_hospital_cases, total_deaths
    return last7day_cases, current_hospital_cases, total_deaths
    

   
    

if __name__ == "__main__":
    get_covid_data("nation","England")

    

