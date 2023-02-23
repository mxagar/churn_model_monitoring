"""This module is in charge of deploying the already
trained and scored model.

The config.json file parametrizes the necessary paths.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
import subprocess
import pickle
import json
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from flask import Flask, session, jsonify, request

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

# "models/development/trained_model.pkl"
model_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['model_filename'])
# "data/ingested/ingested_files.csv"
compilation_record_path = os.path.join(os.getcwd(),
                                       config['output_folder_path'],
                                       config['compilation_record_filename'])
# "models/development/latest_score.csv"
score_path = os.path.join(os.getcwd(),
                          config['output_model_path'],
                          config['score_filename'])
# "models/development/trained_model.pkl"
prod_deployment_path = os.path.join(os.getcwd(),
                                    config['prod_deployment_path'])

def store_model_into_pickle():
    """Store model and related artifacts into
    production folder; altogether, these files are copied
    to the production folder:
    
    - trained model
    - record of ingested files to train it
    - and score records of the trained model
    
    Args: None (all parameters loaded from config.json in global scope)
    Returns: None (specified files are copied to prod folder)
    """
    subprocess.run(["cp", model_path, prod_deployment_path])
    subprocess.run(["cp", compilation_record_path, prod_deployment_path])
    subprocess.run(["cp", score_path, prod_deployment_path])

if __name__ == "__main__":
    store_model_into_pickle()