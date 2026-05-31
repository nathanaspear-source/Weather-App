from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

from preprocess import X, y, X_test, X_train, y_train, y_test, preprocessor


rf = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=1)),
])

rf_parameters = {
    "classifier__max_depth": [10, 20, 30, 40, 50],
    
    "classifier__min_samples_leaf": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "classifier__n_estimators": [50, 100, 200, 300, 500, 1000],
}

rf_grid_search = GridSearchCV(estimator=rf, param_grid=rf_parameters, scoring = "f1_weighted", refit = "True", cv=5, n_jobs=-1, verbose=2)
rf_grid_search.fit(X_train, y_train)

# Storing best performing model for future use
rf_model = rf_grid_search.best_estimator_
joblib.dump(rf_model, "random_forest_model.joblib")

print(f"Best Parameters: {rf_grid_search.best_params_}")
print(f"Best CV score: {rf_grid_search.best_score_:.4f}")
print(f"Test Accuracy: {rf_grid_search.best_estimator_.score(X_test, y_test):.4f}")
print(classification_report(y_test, rf_grid_search.best_estimator_.predict(X_test)))