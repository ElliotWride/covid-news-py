from uk_covid19 import Cov19API
location_filter = [
    'areaType=ltla',
    'areaName=Exeter'
]


cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
    "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
}


def covid_api_request(location_type, location):
    if location_type != location_filter[0][8:]:
        location_filter[0] = "areaType=" + location_type #handles if the location changes
    if location != location_filter[1][8:]:
        location_filter[1] = "areaName=" + location
    api = Cov19API(filters=location_filter, structure=cases_and_deaths)
    data = api.get_csv()

    print(data)

  
covid_api_request("ltla","Exeter")
