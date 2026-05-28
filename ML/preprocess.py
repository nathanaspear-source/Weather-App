import pandas as pd

aus_weather = pd.read_csv('weatherAUS.csv')
print(aus_weather.head())

# Dropping rows with no label value because they cannot be used for model training
aus_weather = aus_weather.dropna(subset="RainTomorrow")

X = aus_weather.drop("RainTomorrow", axis=1)
y = aus_weather["RainTomorrow"]