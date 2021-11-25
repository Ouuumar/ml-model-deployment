# APPLICATION OF BIG DATA

## CLASSIFICATION AND MODEL DEPLOYMENT

## Important note : this project is not focused on the data preparation, but on the tools, frameworks and project architecture used to deploy the app

Including SPHINX documentaion, MLFLOW lifecyle, SHAP model explainer

### STEP 1 : DOWNLOAD THE DATA

Since the csv files are too big to be pushed on GitHub, please download with the link below and do not forget to put csv files in the right folder : "1_rawdata"

<https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv>

### STEP 2 : OPEN A CMD AND CD TO THE PROJECT LOCATION

cd path\to\the\project\location

### STEP 3 : INSTALL DEPENDENCIES

#### Run these commands

pip3 install -r requirements.txt

#### Run the notebooks with nbconvert

Execute each notebook  from 1 to 7

jupyter nbconvert --to notebook --execute mynotebook.ipynb

Then below, you can choose your model (xgBoost.pkl, randomForest.pkl, GradientBoosting.pkl)

python 5_main.py --model "model name"

### STEP 4 : TRACK PARAMETERS AND MODELS IN MLFLOW UI

#### Run this command

mlflow ui

### STEP 5 : OPEN A NEW CMD AND RUN MLFLOW TO DEPLOY A REST SERVER IN ORDER TO MAKE PREDICTION

#### Run these commands

mlflow models serve –-model-uri path\to\the\runexperimentation\artifacts\model --no-conda -p 1234

Or this one below

mlflow models serve –m path\to\the\runexperimentation\artifacts\model --no-conda -p 1234

## STEP 6 : OPEN A NEW CMD TO POST REQUEST

#### Run this command

cd to the project location 

python 6_request.py

#### Documentation

To look at the documentation of the main, open the index.html from the ../docs/hmtl