import requests
from config import API_KEY
from readers import ReaderYAML


class GeoPosition:
    name: str
    lon: str
    lat: str
    main_info: dict
    weather: list
    status: int
    response: str
    geodata_url = "http://api.openweathermap.org/geo/1.0/direct"
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, name, lon="", lat=""):
        self.name = name
        self.lon = lon
        self.lat = lat
        if not self.lon or not self.lat:
            self.get_geodata()
        else:
            self.status = 200

    def get_geodata(self):
        params = {
            "q": self.name,
            "limit": 1,
            "appid": str(API_KEY)
        }
        api_response = requests.get(self.geodata_url, params=params)
        if api_response.status_code == 200:
            for item in api_response.json():
                self.lat = item['lat']
                self.lon = item['lon']
        self.status = api_response.status_code
        self.response = api_response.text

    def __repr__(self):
        return f"{self.name} (lon: {self.lon} lat: {self.lat} )"

    @property
    def obj_data(self):
        return dict(zip(["name", "lat", "lon", "status"], [self.name, self.lat, self.lon, self.status]))

    @obj_data.setter
    def obj_data(self, obj_dict: dict):
        if isinstance(obj_dict, dict):
            self.lon = obj_dict.get("lon")
            self.lat = obj_dict.get("lat")
            self.status = obj_dict.get("status")

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


reader = ReaderYAML("cities.config")
cities = reader.text
cities_obj = []

for i in range(len(cities)):
    if isinstance(cities[i], str):
        new_city = GeoPosition(cities[i])
        cities_obj.append(new_city)
        cities[i] = new_city.obj_data
    elif isinstance(cities[i], dict):
        cities_obj.append(GeoPosition(cities[i].get("name"), lon=cities[i].get("lon"), lat=cities[i].get("lat")))
    else:
        print(type(cities[i]), " : ", cities[i])

    reader.text = cities

for city in cities_obj:
    if city.status == 200:
        city.get_weather()
        print(city.name, "температура:", city.main_info.get('temp'), end=', ')
        print(city.weather[0].get('description'))
    else:
        print("Requests error (weather):", city.status)
        print(city.response)
