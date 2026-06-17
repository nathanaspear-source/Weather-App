import os
import requests
import config
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict
from ML.feature_mapper import FEATURE_COLUMNS, map_openweathermap_to_was

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

def get_weather_data(city: str) -> dict:
    """Returns current weather data for a given city"""
    weather_params = {
        "q": city,
        "appid": api_key,
        "units": "imperial",

    }

    weather_response = requests.get(config.BASE_URL, params = weather_params)
    weather_data = weather_response.json()

    return {
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

def get_weather_forecast(city: str):
    """Returns current weather forecast in Pandas DataFrame for a given city
    using OpenWeatherMap API call (units in metric)"""
    weather_params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    weather_forecast_response = requests.get(config.FORECAST_URL, params=weather_params)
    weather_forecast_data = weather_forecast_response.json()

    days = defaultdict(list)
    for entry in weather_forecast_data["list"]:
        date_key = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
        days[date_key].append(entry)

    rows = {date: map_openweathermap_to_was(entries) for date, entries in days.items()}
    forecast_df = pd.DataFrame.from_dict(rows, orient="index", columns = FEATURE_COLUMNS)
    forecast_df.index.name = "date"

    return forecast_df

def get_weather_forecast_summary(city: str) -> list[dict]:
    """Returns JSON-serializable 5-day forecast for given city.
    (Used for Gemini API calls in chat.py)"""

    df = get_weather_forecast(city)

    keep = [
        "MinTemp", "MaxTemp", "Rainfall", "Humidity9am", "Humidity3pm",
        "WindSpeed9am", "WindSpeed3pm", "RainToday",
    ]

    summary = df[keep].reset_index()
    summary["date"] = summary["date"].astype(str)
    summary = summary.where(pd.notna(summary), None)

    # Converts summary to a list of dictionary where each dictionary
    # is a single row in the list
    return summary.to_dict(orient="records")


def weather_logger(city):
    """Storing weather data in CSV file every 10 minutes"""
    weather = {"timestamp": datetime.now(), **get_weather_data(city)}
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

def safe_weather_logger(city):
    """Logs weather data and isolates errors so long-running background data logging
    doesn't stop"""

    try:
        weather_logger(city)
        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"