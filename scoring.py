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

from training import load_pipeline
from db_setup import Database

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

# "models/development/trained_model.pkl"
model_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['model_filename'])
# "data/test/test_data.csv"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename'])
# "models/development/latest_score.csv"
score_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['score_filename'])
# ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
features = config['features']
target = config['target'] # 'exited'
version = config['version'] # 0.1

def score_model(model_path=model_path,
                data_path=test_data_path,
                score_path=score_path,
                features=features,
                target=target):
    """Score model and save performance metrics.
    Then, save the value to disk.
    
    To that end, the trained model must be loaded, 
    as well as a test dataset.
    
    Args:
        model_path (str): model to be loaded (complete path + filename)
        data_path (str): dataset to be tested (complete path + filename)
        score_path (str): records of scoring (complete path + filename)
        features (list): list of feature columns
        target (str): target column name
    Returns: 
        f1 (float): F1 score
    """
    # Load model pipeline
    estimator = load_pipeline(model_path=model_path)
    
    # Load dataset
    df = pd.read_csv(data_path) # test_data_path
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
    
    # EXTRA: Persist to sqlite database
    # FIXME: we should not instantiate the database every ingestion
    # but rather pass it to the ingestion process...
    db = Database()
    db.insert_score({"model_version": version,
                     "timestamp": datetime.now(),
                     "score_type": "F1",
                     "value": f1})
    # Check: convert to CSV
    scores = db.convert_scores_to_df()
    scores.to_csv('db/scores.csv', sep=',', header=True, index=False)
    db.close()
    
    return f1
    
if __name__ == "__main__":
    _ = score_model(model_path=model_path,
                    data_path=test_data_path,
                    score_path=score_path,
                    features=features,
                    target=target)
