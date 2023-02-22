from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['model_filename']) # "models/development/trained_model.pkl"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename']) # "data/test/test_data.csv"
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'

def load_pipeline():
    """Load pipeline: transformations + model.
    
    Args: None (file path should be in global scope)
    Returns: Pipeline
    """
    return pickle.load(open(model_path,'rb')) # rb: read bytes

def score_model():
    """Score model and save performance metrics
    to 
    """
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file

    # Load model pipeline
    estimator = load_pipeline()
    
    # Load dataset
    df = pd.read_csv(test_data_path)
    X_test = df[features]
    y_test = df[target]

    # Evaluate
    y_pred =  estimator.predict(X_test)
    f1 = metrics.f1_score(y_test, y_pred)
    print(f1)
    
if __name__ == "__main__":
    score_model()
