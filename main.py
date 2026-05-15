import requests
import json
import config

from config import WEATHER_API_KEY

def get_weather_data(city):
    weather_params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "imperial",

    }

    weather_response = requests.get(config.BASE_URL, params = weather_params)
    weather_data = weather_response.json()

    return weather_data