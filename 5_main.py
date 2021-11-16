import os.path as path
from pickle import load, dump
import warnings
import argparse

import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_score(X_test, y_test, model_name):
    """
    X_test : test dataset, y_pred : prediction made, model_name : name of the model desired
    return score of the model
    """
    preds = make_prediction(X_test, model_name)
    clf = load_model(model_name)
    return metrics.accuracy_score(y_test, preds)

def make_prediction(X_test, model_name):
    """
    X_test : test dataset, model_name: name of the model desired
    return the prediction of the model on test set, unseen data
    """
    clf = load_model(model_name)
    return clf.predict(X_test)

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
    # initialize Argument Parser
    parser = argparse.ArgumentParser()
    # we can add any different arguments we want to parse
    parser.add_argument("--model", type=str)
    # we then read the arguments from the comand line
    args = parser.parse_args()
    #save the model in a variable to pass it through functions
    model_name = args.model

    warnings.filterwarnings("ignore")
    np.random.seed(40)

    print("\nInitializing the program\n...")

    X_test = pd.read_csv(path.join("3_X_fitted_dataframe", "X_test_scaled.csv"))
    X_train = pd.read_csv(path.join("3_X_fitted_dataframe", "X_train_scaled.csv"))
    y_train = pd.read_csv(path.join('4_y_dataframe', 'y_train.csv'))   
    y_test = pd.read_csv(path.join('4_y_dataframe', 'y_test.csv'))

    try:
        print("\nData loaded\n...")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s",
        )

    with mlflow.start_run():
        clf = load_model(model_name)
        clf.fit(X_train, y_train)
        score = eval_score(X_test, y_test, model_name)

        mlflow.log_metric("accuracy", score)
        print("\nLogged accuracy\n...")
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        print("\nTracking to MLflow UI\n...")
        
        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            mlflow.sklearn.log_model(clf, "model", registered_model_name=str(model_name))
            print("\nModel registered\n <3")
        else:
            mlflow.sklearn.log_model(clf, "model")
            print("\nModel registered <3\nWithout :registered_model_name=str(model_name): \n...")