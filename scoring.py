"""This module is in charge of scoring the already
trained model using a test dataset.

The config.json file parametrizes the input/output
paths and filenames for all artifacts.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
from datetime import datetime
import pickle
import json
import pandas as pd
#import numpy as np
from sklearn import metrics
#from flask import Flask, session, jsonify, request

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['model_filename']) # "models/development/trained_model.pkl"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename']) # "data/test/test_data.csv"
score_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['score_filename']) # "models/development/latest_score.csv"
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'
version = config['version'] # 0.1

def load_pipeline():
    """Load pipeline: transformations + model.
    
    Args: None (file path should be in global scope)
    Returns: Pipeline
    """
    return pickle.load(open(model_path,'rb')) # rb: read bytes

def score_model():
    """Score model and save performance metrics.
    Then, save the value to disk.
    
    To that end, the trained model must be loaded, 
    as well as a test dataset.
    
    Args: None (file paths should be in global scope)
    Returns: None (results persisted to file in disk)
    """
    # Load model pipeline
    estimator = load_pipeline()
    
    # Load dataset
    df = pd.read_csv(test_data_path)
    X_test = df[features]
    y_test = df[target]

    # Evaluate
    y_pred =  estimator.predict(X_test)
    f1 = metrics.f1_score(y_test, y_pred)
    
    # Pack result and save to disk
    score = {"model_version": [version],
             "timestamp": [datetime.now()],
             "score_type": ["F1"],
             "value": [f1]}
    df_score = pd.DataFrame(score)
    df_score.to_csv(score_path, sep=',', header=True, index=False)
    
if __name__ == "__main__":
    score_model()
