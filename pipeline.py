import os
import subprocess
import json
import zipfile
import time
import papermill as pm
import shutil
import sys
import argparse

start = time.time()

# initialize Argument Parser
parser = argparse.ArgumentParser()
# add model name to parse
parser.add_argument("--model", type=str)
# read the argument from the comand line
args = parser.parse_args()
# save the model in a variable to pass it through functions
MODEL_NAME = args.model

# Configuring global variables for folders and files

FOLDERS = ['1_rawdata', '2_dataprep', '3_X_fitted_dataframe', '4_y_dataframe', '5_fitted_scaler', '6_models']
EXPECTED_DATASETS = ['application_train.csv', 'application_test.csv']

NOTEBOOKS_TO_RUN = ['1_data_preparation.ipynb', '2_feature_engineering.ipynb', '3_model_training.ipynb']
MLFLOW_FILENAME = '4_mlflow.py'
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
          shutil.rmtree(folder) # remove folders of the data in order to re create them if data changed

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

# Getting execution time min, sec.

end = time.time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

print("\n---------------------- EXECUTION TIME ----------------------\n------------------------ {:0>2}:{:0>2}:{:05.2f} ----------------------\n".
format(int(hours),int(minutes),seconds))