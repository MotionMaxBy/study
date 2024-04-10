import requests
import time
from config import API_KEY


def get_geodata(city):
    URL = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": str(API_KEY)
    }
    return requests.get(URL, params=params)


def get_weather(place_lat, place_lon):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": place_lat,
        "lon": place_lon,
        "appid": str(API_KEY),
        "units": "metric",
        "lang": "ru",
    }
    return requests.get(URL, params=params)


response = get_geodata('Гомель')
if response.status_code == 200:
    for city in response.json():
        print(city['local_names']['ru'], city['lat'], ":", city['lon'], end=', ')

        city_weather = get_weather(city["lat"], city["lon"])
        print("Температура:", city_weather.json().get('main').get('temp'), end=', ')
        print(city_weather.json().get('weather')[0].get('description'))
else:
    print("Requests error (weather):", response.status_code)
    print(response.text)
