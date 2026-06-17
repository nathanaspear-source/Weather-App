import streamlit as st
from chat import weather_query

st.set_page_config(
    page_title="Gemini Weather Help",
)

st.header("Gemini Weather Help")
query = st.text_input("Enter Weather Question", key="button_2")

if query:
    weather_response = weather_query(query)
    if weather_response:
        st.write(weather_response)

