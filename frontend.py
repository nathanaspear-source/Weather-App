import streamlit as st
import config
from config import CSV_FILE
from main import get_weather_data
from datetime import datetime, timedelta
import main
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import joblib

def load_rain_model():
    return joblib.load("ML/random_forest_model.joblib")

st.title("Weather App")

city = st.text_input("Enter a City:")

if city:
    st_autorefresh(interval = 60000, key="weather_refresh")
    # Stores last weather update in Streamlit session state
    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.min

    # Saves weather data every minute
    if datetime.now() - st.session_state.last_update > timedelta(minutes=1):
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

    # Select box provided so that users can select what stored weather metric
    # they would like to view as a plot
    plot_option = st.selectbox("Plot Options",
                                ("Temperature", "Humidity", "Pressure", "Wind Speed"))

    st.write("You Selected", plot_option)

    # Plotting temperature over time
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, encoding = "utf-8-sig")
        df.columns = df.columns.str.strip()

        # Sorts each city column's data in DataFrame by the time when it was retrieved
        df = df[df["city"] == city.strip().lower()].sort_values("timestamp")

        # Used to display plot with information corresponding to what the user selected
        if df.empty:
            st.info("No weather data available yet for this city.")
        if not df.empty and plot_option == "Temperature":
            st.line_chart(df, x = "timestamp", y = "temperature")
        if not df.empty and plot_option == "Humidity":
            st.line_chart(df, x = "timestamp", y = "humidity")
        if not df.empty and plot_option == "Pressure":
            st.line_chart(df, x = "timestamp", y = "pressure")
        if not df.empty and plot_option == "Wind Speed":
            st.line_chart(df, x = "timestamp", y = "wind speed")

    # Loads model and predicts whether there will be rain based
    # on weather forecast
    rain_model = load_rain_model()
    forecast_df = main.get_weather_forecast(city)
    predictions = rain_model.predict(forecast_df)

    day_count = min(5, len(predictions))
    cols = st.columns(day_count)

    for i, col in enumerate(cols):
        forecast_date = forecast_df.index[i]
        rain_label = "Rain" if predictions[i] == "Yes" else "No Rain"
        col.metric(label=forecast_date.strptime("%a %b %-d"), value=rain_label)

    # Displays rain forecast (rain or no rain) for next five days
    st.subheader(f"Five Day Rain Forecast")
    col5, col6, col7, col8, col9 = st.columns(5)
    col5.metric(label="Day 1", value=predictions[0])
    col6.metric(label="Day 2", value=predictions[1])
    col7.metric(label="Day 3", value=predictions[2])
    col8.metric(label="Day 4", value=predictions[3])
    col9.metric(label="Day 5", value=predictions[4])