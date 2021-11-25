import pandas as pd
import os
import json
import requests
import subprocess
from pathlib import Path
from subprocess import Popen
import time

MLRUNS_FOLDER = os.path.join('mlruns', '0')
OBSERVATION_IDX = 1

# Run MLFlow Server
ml_folders = sorted(Path(MLRUNS_FOLDER).iterdir(), key=os.path.getmtime)
model_path = os.path.join(ml_folders[-1], 'artifacts', 'model')
print(f"Running model {model_path}")
server = Popen(f"mlflow models serve -m {model_path} --no-conda -p 1234")

print("Waiting for server to run...")
time.sleep(7)

# Send POST request to receive a prediction from the server
df = pd.read_csv(os.path.join('3_X_fitted_dataframe', 'X_test_scaled.csv')).iloc[[OBSERVATION_IDX]]  # Predict with one observation

def invoke(df):
    # POST endpoint '/invocations' ; the data is converted to a JSON format
    response = requests.post("http://127.0.0.1:1234/invocations", data=df[:].to_json(orient="split"), headers={"Content-Type": "application/json; format=pandas-split"})
    return str(response.content)

print(invoke(df))
server.terminate()