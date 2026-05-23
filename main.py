import os
import requests
import json
import config
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

def get_weather_data(city):
    """Returns current weather data for a given city"""
    weather_params = {
        "q": city,
        "appid": api_key,
        "units": "imperial",

    }

    weather_response = requests.get(config.BASE_URL, params = weather_params)
    weather_data = weather_response.json()

    return {
        "timestamp": datetime.now(),
        "city": city.strip().lower(),
        "weather": weather_data["weather"][0]["main"],
        "weather description": weather_data["weather"][0]["description"],
        "temperature": weather_data["main"]["temp"],
        "humidity": weather_data["main"]["humidity"],
        "pressure": weather_data["main"]["pressure"],
        "wind speed": weather_data["wind"]["speed"],
        "wind direction": weather_data["wind"]["deg"],
        "clouds": weather_data["clouds"]["all"],

    }

def weather_logger(city):
    """Storing weather data in CSV file every 10 minutes"""
    weather = get_weather_data(city)
    df = pd.DataFrame([weather])

    file_exists = os.path.isfile(config.CSV_FILE)

    df.to_csv(config.CSV_FILE,
              mode = "a",
              header = not file_exists,
              index = False,
              lineterminator = "\n",
              encoding = "utf-8"
              )
    return weather

if __name__ == "__main__":
    weather_logger()