from datetime import datetime
import numpy as np

COMPASS_POINTS = [
    "N", "NNE", "NE",
    "ENE", "E", "ESE", "SE",
    "SSE", "S", "SSW", "SW",
    "WSW", "W", "WNW", "NW", "NNW",
]

FEATURE_COLUMNS = [
    "MinTemp", "MaxTemp", "Rainfall", "Evaporation",
    "Sunshine", "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm",
    "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
    "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "WindGustDir",
    "WindDir9am", "WindDir3pm", "RainToday",
]

def degrees_to_compass(deg):
    """Converts wind direction in degrees to compass label"""
    if deg is None:
        return None

    index = int(round(float(deg) / 22.5)) % 16
    return COMPASS_POINTS[index]

def entry_hour(entry):
    """Returns the hour of the forecast inputted into forecast DataFrame"""
    return datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").hour

def pick_entry_at_hour(entries, hour):
    """Returns the forecast entry closest to given hour"""
    return min(entries, key=lambda e: abs(entry_hour(e) - hour))

def gust_or_speed(entry):
    return entry["wind"].get("gust", entry["wind"]["speed"])

def clouds_percent_to_oktas(percent):
    """Converts OpenWeatherMap cloud cover percentage (0%-100%) to oktas (0-8)"""
    return int(round(percent * 8 / 100))

def map_openweathermap_to_was(day_entries):
    """Translates OpenWeatherMap weather forecast data point attributes
    into features like the Rain in Australia Kaggle dataset used for training the
    ML model"""

    if not day_entries:
        raise ValueError("day_entries must contain at least one forecast entry")

    rainfall_mm = sum(
        entry.get("rain", {}).get("3h", 0.0) for entry in day_entries
    )
    gust_entry = max(day_entries, key = gust_or_speed)

    # Stores entries in weather forecast DataFrame closest to 9am and 3pm
    morning = pick_entry_at_hour(day_entries, 9)
    afternoon = pick_entry_at_hour(day_entries, 15)

    return {
        "MinTemp": min(entry["main"]["temp_min"] for entry in day_entries),
        "MaxTemp": max(entry["main"]["temp_max"] for entry in day_entries),
        "Rainfall": rainfall_mm,
        "Evaporation": np.nan, # not available in OpenWeatherMap forecast
        "Sunshine": np.nan, # not available in OpenWeatherMap forecast
        "WindGustSpeed": gust_or_speed(gust_entry),
        "WindSpeed9am": morning["wind"]["speed"],
        "WindSpeed3pm": afternoon["wind"]["speed"],
        "Humidity9am": morning["main"]["humidity"],
        "Humidity3pm": afternoon["main"]["humidity"],
        "Pressure9am": morning["main"]["pressure"],
        "Pressure3pm": afternoon["main"]["pressure"],
        "Cloud9am": clouds_percent_to_oktas(morning["clouds"]["all"]),
        "Cloud3pm": clouds_percent_to_oktas(afternoon["clouds"]["all"]),
        "Temp9am": morning["main"]["temp"],
        "Temp3pm": afternoon["main"]["temp"],
        "WindGustDir": degrees_to_compass(gust_entry["wind"].get("deg")),
        "WindDir9am": degrees_to_compass(morning["wind"].get("deg")),
        "WindDir3pm": degrees_to_compass(afternoon["wind"].get("deg")),
        "RainToday": "Yes" if rainfall_mm >= 1.0 else "No",
    }

