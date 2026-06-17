import joblib
def load_rain_model():
    """Loads rain prediction model"""
    return joblib.load("ML/random_forest_model.joblib")