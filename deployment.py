"""This module is in charge of deploying the already
trained and scored model.

The config.json file parametrizes the necessary paths.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
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

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 

def store_model_into_pickle(model):
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory

if __nanme__ == "__main__":
    store_model_into_pickle()