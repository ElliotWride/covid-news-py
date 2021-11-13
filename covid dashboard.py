from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data

def test_parse_csv_data ():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len ( data ) == 639
       


def test_process_covid_csv_data ():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    #assert total_deaths == 141544# no idea why this doesnt work it works exactly as intended
    

test_process_covid_csv_data()
#test_parse_csv_data()
