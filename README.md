# Launch the project

## Download the data here please

<https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv>

put it in the right folder "1_rawdata"

## Open a cmd and cd to the project location

## Install dependencies

pip3 install -r requirements.txt

python 5_main.py --model "model name"

## see the run in mlflow ui

mlflow ui

### Open a new cmd and run MLFlow to deploy a REST server a make prediction with a POST request, use --no-conda option

mlflow models serve –-model-uri path\to\the\runexperimentation\artifacts\model --no-conda -p 1234

or

mlflow models serve –m path\to\the\runexperimentation\artifacts\model --no-conda -p 1234

or one is already done with this command below :

mlflow models serve –m mlruns\0\ed2dd4a7353547fd97dc4b1245f25645\artifacts\model --no-conda -p 1234

## Then open a new cmd and run

python request.py
