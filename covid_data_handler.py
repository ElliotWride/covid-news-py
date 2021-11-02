from datetime import date


def parse_csv_data(*name):
    with open(str(name[0])) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def process_covid__csv_data():
    covid_csv_data = parse_csv_data('nation_2021-10-28.csv')
    #print(covid_csv_data)
    today =  '15/10/2021'
    last7day_cases = 0
    
    for index in range (0, len(covid_csv_data)):
        if today in covid_csv_data[index].split(","):
            current_hospital_cases = covid_csv_data[index].split(",")[4]
            total_deaths = covid_csv_data[index].split(",")[5]
            for i in range (0,7):
                last7day_cases += int(covid_csv_data[index+i].split(",")[6])
    print(last7day_cases)
    print(current_hospital_cases)
    print(total_deaths)
    
    
    
    
    
    
#process_covid_data()
    


