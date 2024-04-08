import requests
import time


def read_file(file_path: str):
    try:
        with open(file_path, "r") as f:
            res = f.read().strip()
    except Exception as e:
        print(e)
        return None
    return res


api_key = read_file("api_key.txt")

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

