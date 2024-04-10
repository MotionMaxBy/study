import requests
import time
from config import API_KEY


api_key = str(API_KEY)

URL = "http://api.openweathermap.org/geo/1.0/direct"

params = {
    "q": "Гомель",
    "limit": 1,
    "appid": api_key
}


response = requests.get(URL, params=params)
if response.status_code == 200:
    for place in response.json():
        # print(place)
        print("{} ({}:{})".format(place["local_names"]["ru"], place["lat"], place["lon"]))

        URL = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": place["lat"],
            "lon": place["lon"],
            "appid": api_key,
            "units": "metric",
            "lang": "ru",
        }

        time.sleep(1.2)
        response = requests.get(URL, params=params)
        if response.status_code == 200:
            for key in response.json().keys():
                print(f"{key}:", response.json()[key])
        else:
            print("Requests error (weather):", response.status_code)
            print(response.text)
else:
    print("Request error:", response.status_code)

