import requests
import json
import click
from statistics import median, mode


def get_kpis_metadata(kpi_list, start, stop):
    kpi_names_to_index_map = {
        'date': 0,
        'temperature': (1, []),
        'humidity': (2, []),
        'light': (3, []),
        'co2': (4, []),
        'humidityratio': (5, []),
        'occupancy': (6, []),
    }
    kpis_metadata_results = {
        'temperature': {},
        'humidity': {},
        'light': {},
        'co2': {},
        'humidityratio': {},
        'occupancy': {},
    }
    kpis_url = 'http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(kpis_url, headers=headers)
    if not response.content:
        return 'Something went wrong.'  # something went wrong
    response_body = json.loads(response.content)
    while response_body['data'].strip() == "":  # sometimes response contains no data
        response = requests.get(kpis_url, headers=headers)
        response_body = json.loads(response.content)
    if not response_body['ok']:
        return 'Something went wrong.'  # something went wrong
    list_of_kpis_info = response_body['data'].split('\n')[1:]  # list of data; its form: date,Temperature,Humidity,Light,CO2,HumidityRatio,Occupancy
    kpis_within_timeframe = []
    for kpi in list_of_kpis_info:  # let's collect all kpis within given timeframe
        kpi_date = kpi.split(',')[0]  # date extraction
        if kpi_date >= start and kpi_date <= stop:
            kpis_within_timeframe.append(kpi)
    for needed_kpi in kpi_list:
        needed_kpi_index = kpi_names_to_index_map[needed_kpi][0]
        for kpi in kpis_within_timeframe:
            kpi_names_to_index_map[needed_kpi][1].append(float(kpi.split(',')[needed_kpi_index]))
        # now let's do analysis on certain kpi category
        list_of_certain_categories = kpi_names_to_index_map[needed_kpi][1]
        category_resulting_dict = {
            'last_value': list_of_certain_categories[-1],
            'first_value': list_of_certain_categories[0],
            'lowest': min(list_of_certain_categories),
            'highest': max(list_of_certain_categories),
            'mode': mode(list_of_certain_categories),
            'average': sum(list_of_certain_categories) / len(kpi_names_to_index_map[needed_kpi][1]),
            'median': median(list_of_certain_categories)
        }
        kpis_metadata_results[needed_kpi] = category_resulting_dict
    return kpis_metadata_results



if __name__ == '__main__':
    print(get_kpis_metadata(['light', 'occupancy'], '2/2/15 14:37', '2/3/15 0:15'))
