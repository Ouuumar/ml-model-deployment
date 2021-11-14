# Launch the project

# Download the data here please

<https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv>

put it in the right folder "1_rawdata"

## cd to the project location

## Install dependencies

pip3 install -r requirements.txt

python 5_main.py

## see the run in mlflow ui

mlflow ui

### To run MLFlow, use --no-conda option

mlflow models serve –-model-uri path\to\the\runexperimentation\artifacts\model --no-conda -p 1234

or one is already done with this command below :

mlflow models serve –-model-uri mlruns\0\a2c8f45154d44055a677edbda577c157\artifacts\model --no-conda -p 1234
