# **APPLICATION OF BIG DATA**

## CLASSIFICATION AND MODEL DEPLOYMENT

====================================

### **Fully automated pipeline**, making data preparation, feature engineering, model training, predicting and scoring (should run once)

====================================

#### **MLflow automated deployment**, tracking parameters and make POST request to predict

====================================

#### **Important note** : this project is not focused on the data preparation, but on the tools, frameworks and project architecture used to deploy the app

====================================

# How to execute the project ?

**Important note** : since I use my own kaggle token, it may disapear, and you will need to get your own kaggle key, to download datasets from Kaggle

To get this kaggle key, sign in your kaggle account, go to your profil pic

- click on "Your profile"
- click on "Account"
- click on "Create new token API", in the API section
- **Save the json content in the kaggle.json (just copy paste your token in the existing file)**

## Run these commands, open as admin a CMD and then, cd to the project location

====================================

- Run **pip3 install -r requirements.txt**

====================================

While the pipeline will train 3 models, it will only use the model given in input for logs and predictions

- Run **python pipeline.py --model "model_name_desired"**
- (among xgBoost.pkl, randomForest.pkl, GradientBoosting.pkl, precise in the argument the **.pkl** and without double "quotes")

====================================

This pipeline is up to few minutes execution (depends on your compute power), so feel free to do something else on the side or watch the process and logs :)

====================================

## When the pipeline is done

====================================

### Want to only do simple train and test models ?

====================================

- Run **python 4_mlflow.py --model "model_name_desired"**
- (among xgBoost.pkl, randomForest.pkl, GradientBoosting.pkl, precise in the argument the **.pkl** and without double "quotes" please)

- Run **mlflow ui** and open your local host
- Watch experimentations runs and logged metric

====================================

### Maybe also want to only predict on the REST server ?

====================================

- Run **python 5_request.py** 
- (it will launch, predict and then automatically stop the REST server)

====================================

#### Documentation

## The documentation is a simple test and was made with the previous project version

====================================

To look at the documentation of the main, open the index.html from the **./docs/hmtl**
