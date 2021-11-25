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
    :param name: X_test - test dataset y_pred - prediction made model_name - name of the model desired
    :return: accuracy of the model
    """
    preds = make_prediction(X_test, model_name)
    clf = load_model(model_name)
    return metrics.accuracy_score(y_test, preds)

def make_prediction(X_test, model_name):
    """
    :param name: X_test - test dataset model_name - name of the model desired
    :return: the prediction of the model on test set, unseen data
    """
    clf = load_model(model_name)
    return clf.predict(X_test)

def load_model(model_name):
    """
    :param name: model_name - name of the model desired
    :return: the model desired loaded
    """
    return load(open(path.join('6_models', "{}").format(model_name), 'rb'))

def load_datasets():
    """
    :return: the train and test datasets, X, y
    """
    X_test = pd.read_csv(path.join("3_X_fitted_dataframe", "X_test_scaled.csv"))
    X_train = pd.read_csv(path.join("3_X_fitted_dataframe", "X_train_scaled_resamp.csv"))
    y_train = pd.read_csv(path.join('4_y_dataframe', 'y_train_resamp.csv'))   
    y_test = pd.read_csv(path.join('4_y_dataframe', 'y_test.csv'))

    try:
        print("\nData loaded\n...")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s",
        )
    return X_test, X_train, y_train, y_test


if __name__ == "__main__":
    """
    main loop to train, predict and score our models
    Pass it the model desired as an argument with --model
    """
    # initialize Argument Parser
    parser = argparse.ArgumentParser()
    # add model name to parse
    parser.add_argument("--model", type=str)
    # read the argument from the comand line
    args = parser.parse_args()
    # save the model in a variable to pass it through functions
    model_name = args.model

    warnings.filterwarnings("ignore")
    np.random.seed(40)

    print("\nInitializing the program\n...")

    # Assign our datasets and load them
    X_test, X_train, y_train, y_test = load_datasets()

    # Start the mlflow run, to fit, and score
    with mlflow.start_run():
        clf = load_model(model_name)
        clf.fit(X_train, y_train)

        score = eval_score(X_test, y_test, model_name)
        mlflow.log_metric("accuracy", score)
        print("\nLogged accuracy\n...")

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        print("\nTracking to MLflow UI\n...")

        mlflow.sklearn.log_model(clf, "model")
        print("\nModel registered <3\n...")

