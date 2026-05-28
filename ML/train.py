import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from preprocess import X, y


rf = RandomForestClassifier(n_estimators = 100, random_state = 1)

rf_parameters = {
    "max_depth": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    "min_samples_leaf": [1, 2, 3, 4, 5, 6, 7, 8, 9],
}

rf_grid_search = GridSearchCV(estimator=rf, param_grid=rf_parameters, refit = "True", cv=5, n_jobs=-1)
rf_grid_search.fit(X, y)

rf_model = rf_grid_search.best_estimator_

print(f"Best Parameters: {rf_grid_search.best_params_}")
print(f"Best CV score: {rf_grid_search.best_score_}:.4f")
print(f"Training Accuracy: {rf_grid_search.score(X, y):.4f}")