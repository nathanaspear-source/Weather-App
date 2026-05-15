import streamlit as st
import config
from config import CSV_FILE
from main import get_weather_data
from datetime import datetime, timedelta
import main
import os
import pandas as pd


st.title("Weather App")

city = st.text_input("Enter a City:")

if city:
    # Stores last weather update in Streamlit session state
    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.min

    # Saves weather data every 10 minutes
    if datetime.now() - st.session_state.last_update > timedelta(minutes=10):
        weather = main.weather_logger(city)
        st.session_state.last_update = datetime.now()
        st.success("Weather data saved")

    weather = get_weather_data(city)

    # Displays header, city, and most important weather data
    st.header(f"Weather Data for {city.capitalize()}")
    st.subheader(f"Today's Weather Will Have {weather['weather']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label = "Temperature", value = f"{weather['temperature']}°F")
    col2.metric(label = "Humidity", value = f"{weather['humidity']}%")
    col3.metric(label = "Wind Speed", value = f"{weather['wind speed']} mph")
    col4.metric(label = "Wind Direction", value = f"{weather['wind direction']}°")

    # Plotting temperature over time
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, encoding = "utf-8-sig")
        df.columns = df.columns.str.strip()

        if "timestamp" in df.columns and "temperature" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
            df = df.dropna(subset=["timestamp", "temperature"])

            if not df.empty:
                st.line_chart(df, x = "timestamp", y = "temperature")

