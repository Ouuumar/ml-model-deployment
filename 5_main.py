import os.path as path
from pickle import load, dump
import warnings

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_score(X_test, y_test):
    """
    X_test : test dataset, y_pred : prediction made, model_name : name of the model desired
    return score of the model
    """
    clf = load_model("xgBoost.pkl")
    return clf.score(X_test, y_test)

def load_model(model_name):
    """
    model_name : name of the model desired
    return the model desired
    """
    return load(open(path.join('6_models', "{}").format(model_name), 'rb'))


if __name__ == "__main__":
    """
    main loop to train, predict and score our models
    """
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    X_test = pd.read_csv(path.join("3_X_fitted_dataframe", "X_test_scaled.csv"))
    X_train = pd.read_csv(path.join("3_X_fitted_dataframe", "X_train_scaled.csv"))
    y_train = pd.read_csv(path.join('4_y_dataframe', 'y_train.csv'))   
    y_test = pd.read_csv(path.join('4_y_dataframe', 'y_test.csv'))   


    try:
        print("\nData loaded\n")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    with mlflow.start_run():
        clf = load_model("xgBoost.pkl")
        clf.fit(X_train, y_train)

        predicted = clf.predict(X_test)

        score = eval_score(X_test, y_test) # should be y_test
        mlflow.log_param("score", score)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            mlflow.sklearn.log_model(clf, "model", registered_model_name="xgBoost")
        else:
            mlflow.sklearn.log_model(clf, "model")
