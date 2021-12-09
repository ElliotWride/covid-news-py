'''Gets data from the Cov19API and processes the relevant information'''
from uk_covid19 import Cov19API
data_structure_JSON = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType" : "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
    "hospitalCases" : "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
}


def covid_api_request(location_type = "ltla", location = "Exeter"):
    '''Requests data from the API from a certain place'''
    location_filter = ["areaType="+location_type,"areaName="+location]
    api = Cov19API(filters=location_filter, structure=data_structure_JSON)
    data = api.get_json()
    return data


def parse_csv_data(csv_file_name):
    '''processes a file by converting lines to an array'''
    with open(csv_file_name) as file:
        lines = file.readlines()
    return lines


def process_covid_csv_data(covid_csv_data):
    '''will process relevent data from a csv file'''
    last7day_cases = 0
    total_deaths = 0
    current_hospital_cases = 0
    for i in range (3,10):
        if covid_csv_data[i].split(",")[6] != "\n":
            last7day_cases += int(covid_csv_data[i].split(",")[6])
    current_hospital_cases = int(covid_csv_data[i].split(",")[5])
    j = 0
    while True:
        '''continiously tries to convert row 4 of the table into an integer
        if it fails it goes to the next column and tries again'''
        try:
            total_deaths = int(covid_csv_data[j].split(",")[4])
            break #when the first integer value is found the loop stops
        except:
            j = j+1
    return last7day_cases, current_hospital_cases, total_deaths


def get_covid_data(location_type= "ltla", location = "Exeter", nation = "England"):
    '''Gets and processes a JSON file of covid data'''
    local_data = covid_api_request(location_type,location)
    national_data = covid_api_request("nation",nation)
    total_deaths = 0
    #finds first value in "cumDailyNsoDeathsByDeathDate"
    for dic in local_data["data"]:
        if dic["cumDailyNsoDeathsByDeathDate"] is not None:
            total_deaths = dic["cumDailyNsoDeathsByDeathDate"]
            break

    #finds first value in "hospitalCases"
    current_hospital_cases = 0
    for dic in local_data["data"]:
        if dic["hospitalCases"] is not None:
            current_hospital_cases = dic["hospitalCases"]
            break

    #finds the total sum of "newCasesBySpecimenDate" for last 7 days
    days = 0
    local_last7day_cases = 0
    for dic in local_data["data"]:
        if dic["newCasesBySpecimenDate"] is not None:
            days +=1
            local_last7day_cases += dic["newCasesBySpecimenDate"]
        if days == 7:
            break

    days = 0
    national_last7day_cases = 0
    for dic in national_data["data"]:
        if dic["newCasesBySpecimenDate"] is not None:
            days +=1
            national_last7day_cases += dic["newCasesBySpecimenDate"]
        if days == 7:
            break

    return national_last7day_cases, local_last7day_cases, current_hospital_cases, total_deaths





if __name__ == "__main__":
    process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv '))
