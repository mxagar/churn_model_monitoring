"""This module is in charge of training
a logistic regression model on the merged dataset.

The config.json file parametrizes the input/output
paths for the data/model.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
import json
import pickle
import pandas as pd
#import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
#from flask import Flask, session, jsonify, request

# Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(os.getcwd(),
                                config['output_folder_path'],
                                config['compiled_data_filename']) # "data/ingested/final_data.csv"
model_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['model_filename']) # "models/development/trained_model.pkl"
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'
random_seed = config['random_seed']
test_size = config['test_size']

def save_pipeline(pipe):
    """Persist pipeline: transformations + model.
    
    Args: None (file path should be in global scope)
    Returns: None (artifact persisted)
    """
    pickle.dump(pipe, open(model_path,'wb')) # wb: write bytes

def train_model():
    """Define the inference pipeline and fit it to the data.
    The pipeline consists of a scaler and a logistic
    regression model.
    
    Args: None (defined in the global scope, taken from config.json)
    Returns: None (pipeline persisted to file)
    """
    # Instantiate logistic regression model
    # FIXME: LogisticRegression parameters should be in the config.json/yaml
    # FIXME: hyperparameter tuning is not considered here
    # FIXME: in a general situation, we'd define a Pipeline with more transformations...
    estimator = Pipeline([
        ("scaler", StandardScaler()),
        ("logistic_regression", LogisticRegression(
            C=1.0,
            class_weight=None,
            dual=False,
            fit_intercept=True,
            intercept_scaling=1,
            l1_ratio=None,
            max_iter=100,
            #multi_class='warn',
            n_jobs=None,
            penalty='l2',
            random_state=0,
            solver='liblinear',
            tol=0.0001,
            verbose=random_seed,
            warm_start=False)
         )])
    
    # Load dataset
    df = pd.read_csv(dataset_csv_path)
    
    # Split
    # FIXME: splitting doesn't make much sense currently,
    # but we could use it to create X_val, y_val instead
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size, 
        random_state=random_seed,
        stratify=y
    )
    
    # Train
    estimator.fit(X_train, y_train)
    
    # Evaluate
    # FIXME: This test split is not used for evaluation,
    # instead socring.py uses a dedicated dataset
    y_pred =  estimator.predict(X_test)
    _ = metrics.f1_score(y_test, y_pred)
    
    # Persist pipeline/model
    save_pipeline(estimator)

if __name__ == "__main__":
    train_model()