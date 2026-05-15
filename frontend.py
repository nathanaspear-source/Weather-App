import streamlit as st
import config
from main import get_weather_data

st.title("Weather App")

city = st.text_input("Enter a City:")

if city:
    st.header(f"Weather Data for {city.capitalize()}")
    weather = get_weather_data(city)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border = True):
            st.metric("Temperature", f"{weather["main"]["temp"]}°F")

    with col2:
        with st.container(border = True):
            st.metric("Humidity", f"{weather["main"]["humidity"]} W")

    with col3:
        with st.container(border = True):
            st.metric("Wind Speed", f"{weather["wind"]["speed"]} mph")

    with col4:
        with st.container(border = True):
            st.metric("Wind Direction", f"{weather['wind']['deg']}°")


