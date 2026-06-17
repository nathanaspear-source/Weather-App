from google import genai
from google.genai import types
from dotenv import load_dotenv

from main import get_weather_data, get_weather_forecast_summary



# Loads Google AI API key and avoids leaking it
load_dotenv()

AI_CONTEXT = ("You are a helpful assistant to help users understand weather data. Keep answers helpful, factual, and brief (under 5 sentences). "
              "When the user asks about a specific city, call get_weather_data for current weather conditions or get_weather_forecast_summary for "
              "a forecast of the next 5 days in that city.")

def weather_query(query):
    """Uses Google AI Studio AI SDK to return response to inputted query"""
    client = genai.Client()
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = query,
        config = types.GenerateContentConfig(
            system_instruction=AI_CONTEXT,
            tools=[get_weather_data, get_weather_forecast_summary],
        ),
    )

    return response.text