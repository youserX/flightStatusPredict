from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

user_key = 'cb1715c8ae2545f4814fc4e129315de6'
root = 'https://free-api.heweather.com/s6/weather/forecast?location='
_windDri = {
        'N': 1, 'NNE': 2, 'NE': 3, 'ENE': 4,
        'E': 5, 'ESE': 6, 'SE': 7, 'SSE': 8,
        'S': 9, 'SSW': 10, 'SW': 11, 'WSW': 12,
        'W': 13,  'WNW': 14, 'NW': 15, 'NNW': 16
    }

def shanghai_weather():
    location = 'CN101020100'
    return get_weather(location)


def paris_weather():
    location = 'FR2988507'
    return get_weather(location)

def get_weather(loc):
    url = root + loc + '&key=' + user_key + '&lang=en'
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'lxml')
    content = soup.p.get_text()
    #print(content)
    json_content2 = json.loads(content)
    #print(type(json_content2))
    #print('----------------')
    forecast = json_content2['HeWeather6'][0]['daily_forecast']
    #print(forecast)
    _factor = get_factors(forecast)
    return _factor


def get_factors(forecast):
    i = 0
    _Humidity = []
    _Pressure = []
    _Visibility = []
    _Wind_DirN = []
    _Wind_Speed = []
    while i < 3:
        _Humidity.append(int(forecast[i]['hum']))
        _Pressure.append(int(forecast[i]['pres']))
        _Visibility.append(int(forecast[i]['vis']))
        _wind_dri = str(forecast[i]['wind_dir'])
        _Wind_DirN.append(_windDri[_wind_dri])
        _Wind_Speed.append(int(forecast[i]['wind_spd']))
        i = i + 1
    _factor = pd.DataFrame({"Humidity": _Humidity, "Pressure": _Pressure, "Visibility": _Visibility,
                            'Wind Dir': _Wind_DirN, 'Wind Speed': _Wind_Speed})
    print(_factor)
    return _factor


def get_date():
    url = root + 'CN101020100' + '&key=' + user_key + '&lang=en'
    re = requests.get(url)
    page = re.text
    soup = BeautifulSoup(page, 'lxml')
    content = soup.p.get_text()
    #print(content)
    json_content2 = json.loads(content)
    #print(type(json_content2))
    #print('----------------')
    forecast = json_content2['HeWeather6'][0]['daily_forecast']
    i = 0
    dates = []
    while i < 3:
        date = forecast[i]['date']
        dates.append(date)
        i = i+1
    print(dates)
    return dates
