import os.path as path
from pickle import load, dump
import warnings
import argparse

import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support as score
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
    precision, recall, fscore, support = score(y_test, preds)
    accuracy = metrics.accuracy_score(y_test, preds)
    return accuracy, precision, recall, fscore, support

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

        accuracy, precision, recall, fscore, support = eval_score(X_test, y_test, model_name)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision[0])
        mlflow.log_metric("recall", recall[0])
        mlflow.log_metric("fscore", fscore[0])
        mlflow.log_metric("Nb y_true", support[0])
        mlflow.log_metric("Nb y_false", support[1])
        print("\nLogged metrics\n...")

        params = clf.get_params()

        # Set wanted metrics
        par1 = params.fromkeys(['objective'], params['objective']) 
        par2 = params.fromkeys(['learning_rate'], params['learning_rate'])
        par3 = params.fromkeys(['max_depth'], params['max_depth'])
        par4 = params.fromkeys(['random_state'], params['random_state'])

        # Concatenate them
        par1.update(par2)
        par1.update(par3)
        par1.update(par4)

        mlflow.log_params(par1)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        print("\nTracking to MLflow UI\n...")

        mlflow.sklearn.log_model(clf, "model")
        print("\nModel registered <3\n...")

