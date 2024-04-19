import requests
import json
import time
from config import API_KEY


class GeoPosition:
    name: str
    lon: str
    lat: str
    local_names: list
    main_info: dict
    weather: list
    status: int
    response: str
    geodata_url = "http://api.openweathermap.org/geo/1.0/direct"
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, name):
        self.name = name

    def get_geodata(self):
        params = {
            "q": self.name,
            "limit": 1,
            "appid": str(API_KEY)
        }
        api_response = requests.get(self.geodata_url, params=params)
        if api_response.status_code == 200:
            for place in api_response.json():
                self.local_names = place['local_names']
                self.lat = place['lat']
                self.lon = place['lon']
        self.status = api_response.status_code
        self.response = api_response.text

    def __repr__(self):
        return f"{self.name} (lon: {self.lon} lat: {self.lat} )"

    @property
    def json(self):
        return json.dumps({self.name: {"lon": self.lon, "lat": self.lat, "local_names": self.local_names}})

    @json.setter
    def json(self, json_dict):
        for key, value in json_dict.values():
            self.name = key
            self.lat = value.get("lat")
            self.lon = value.get("lon")
            self.local_names = value.get("local_names")

    def get_weather(self):
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": str(API_KEY),
            "units": "metric",
            "lang": "ru",
        }
        api_weather_response = requests.get(self.weather_url, params=params)
        if api_weather_response.status_code == 200:
            self.main_info = api_weather_response.json().get('main')
            self.weather = api_weather_response.json().get('weather')


city = GeoPosition('Гомель')
city.get_geodata()

if city.status == 200:
    city.get_weather()
    print(city.name, "температура:", city.main_info.get('temp'), end=', ')
    print(city.weather[0].get('description'))
else:
    print("Requests error (weather):", city.status)
    print(city.response)
