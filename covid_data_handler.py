from datetime import date


def parse_csv_data(*name):
    with open(str(name[0])) as file:
        lines = file.readlines()
    return lines

def process_covid_csv_data(covid_csv_data):
   
    #print(covid_csv_data)
    today =  '28/10/2021'
    last7day_cases = 0
    
    for index in range (0, len(covid_csv_data)):
        if today in covid_csv_data[index].split(","):
            current_hospital_cases = covid_csv_data[index].split(",")[5]
            total_deaths = covid_csv_data[index].split(",")[4]
            for i in range (0,7):
                last7day_cases += int(covid_csv_data[index+i+1].split(",")[6])
    return int(last7day_cases), current_hospital_cases, total_deaths
    
    
    
    
    
#process_covid_data()
    


