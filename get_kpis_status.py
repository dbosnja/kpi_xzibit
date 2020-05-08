import requests
import json
import click


kpis_url = 'http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
headers = {
    'User-Agent': user_agent
}
def get_kpi_response(url=kpis_url, headers=headers):
    response = requests.get(url=url, headers=headers)
    response_body = json.loads(response.content)
    while response_body['data'].strip() == "":  # sometimes response contain no data
        response = requests.get(url=url, headers=headers)
        response_body = json.loads(response.content)
    if not response_body['ok']:
        return False  # something went wrong
    kpis_list = response_body['data'].split('\n')[1:]  # list of data, form: date,Temperature,Humidity,Light,CO2,HumidityRatio,Occupancy
    return kpis_list

if __name__ == '__main__':
    print(get_kpi_response())
