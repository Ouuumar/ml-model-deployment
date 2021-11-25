import os
import subprocess
import json
import zipfile
import time
import papermill as pm
import shutil
import sys

FOLDERS = ['1_rawdata', '2_dataprep', '3_X_fitted_dataframe', '4_y_dataframe', '5_fitted_scaler', '6_models']
EXPECTED_DATASETS = ['application_train.csv', 'application_test.csv']

NOTEBOOKS_TO_RUN = ['1_data_preparation.ipynb', '2_feature_engineering.ipynb', '3_model_training.ipynb']
MLFLOW_FILENAME = '4_mlflow.py'
MODEL_NAME = "xgBoost.pkl"
REQUEST_FILENAME = '5_request.py'
NOTEBOOK_FINAL_FILENAME = '6_explainer.ipynb'

PAPERMILL_PARAMS = {
    "progress_bar": True,
    "log_output": True,
    "stdout_file": sys.stdout,
    "stderr_file": sys.stderr
}

# Create Data FOLDERS

for folder in FOLDERS:
    try:
        if os.path.exists(folder):
          shutil.rmtree(folder)

        os.mkdir(folder)
    except OSError:
        print ("Creation of the directory %s failed" % folder)    


# Download Kaggle Files
with open('kaggle.json', 'r') as file:
  kaggle_key = json.loads(file.read())

os.environ['KAGGLE_USERNAME'] = kaggle_key['username']
os.environ['KAGGLE_KEY'] = kaggle_key['key']
os.chdir(FOLDERS[0])

if not all(os.path.isfile(file) for file in EXPECTED_DATASETS):
  from kaggle.api.kaggle_api_extended import KaggleApi

  api = KaggleApi()
  api.authenticate()

  for file in EXPECTED_DATASETS:
    if(not os.path.isfile(file)):
      api.competition_download_file('home-credit-default-risk',file)
      with zipfile.ZipFile(f'{file}.zip', 'r') as zip_file:
        zip_file.extractall()
      os.remove(f'{file}.zip')

os.chdir('..')


# Run Notebooks
for nb in NOTEBOOKS_TO_RUN:
  pm.execute_notebook(
    nb,
    nb,
    **PAPERMILL_PARAMS
  )


# Run Main
subprocess.run(f"python {MLFLOW_FILENAME} --model {MODEL_NAME}")


# Run Request
subprocess.run(f"python {REQUEST_FILENAME}")


# Run Results Notebook
pm.execute_notebook(
  NOTEBOOK_FINAL_FILENAME,
  NOTEBOOK_FINAL_FILENAME,
  **PAPERMILL_PARAMS
)