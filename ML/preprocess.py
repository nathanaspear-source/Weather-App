import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

aus_weather = pd.read_csv('weatherAUS.csv')
print(aus_weather.head())

# Dropping rows with no label value because they cannot be used for model training
aus_weather = aus_weather.dropna(subset="RainTomorrow")

# Dropping date and location columns
aus_weather = aus_weather.drop("Date", axis=1)
aus_weather = aus_weather.drop("Location", axis=1)

# Separating dataset into features and label DataFrames
X = aus_weather.drop("RainTomorrow", axis=1)
y = aus_weather["RainTomorrow"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Inputting NAN values in feature DataFrame
num_features = ["MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm",
                "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm"]

cat_features = ["WindGustDir", "WindDir9am", "WindDir3pm", "RainToday"]

num_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

cat_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))

])

# Combining numeric and categorical preprocessing steps into pipeline
preprocessor = ColumnTransformer([
    ("num", num_transformer, num_features),
    ("cat", cat_transformer, cat_features),
])