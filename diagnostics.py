"""This module is in charge of running diagnostics
of several components in the system:

- Model predictions
- Training dataset statistics, i.e., column means, NAs, etc.
- Timing for ingestion and training
- Dependencies

The config.json file parametrizes the necessary paths
and filenames.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import timeit
import os
import json
import pandas as pd
import numpy as np

from training import load_pipeline

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f)

# "data/ingested/final_data.csv"
dataset_csv_path = os.path.join(os.getcwd(),
                                config['output_folder_path'],
                                config['compiled_data_filename'])
# "models/production/trained_model.pkl"
model_path = os.path.join(os.getcwd(),
                          config['prod_deployment_path'],
                          config['model_filename'])
# "data/test/test_data.csv"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename'])
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'

def model_predictions():
    """Predict outcomes for the test dataset
    using the trained model.
    
    Necessary parameters are in the global scope,
    loaded from config.json.

    Args: None (all paths in the global scope, loaded from config.json)
    Returns:
        y_pred (list): predictions for the test dataset
        y_test (list): ground truth target values
    """
    # Load model pipeline
    estimator = load_pipeline(model_path=model_path)
    
    # Load dataset
    df = pd.read_csv(test_data_path)
    X_test = df[features]
    y_test = list(df[target].values.ravel())
    
    # Predict
    y_pred = list(estimator.predict(X_test).reshape(1,-1).ravel())
    
    return y_pred, y_test
    
def dataframe_summary():
    """Predict outcomes for the test dataset
    using the trained model.
    
    Necessary parameters are in the global scope,
    loaded from config.json.

    Args: None (all paths in the global scope, loaded from config.json)
    Returns:
        y_pred (list): predictions for the test dataset
    """    #calculate summary statistics here
    #return value should be a list containing all summary statistics
    pass

def missing_data():
    """Predict outcomes for the test dataset
    using the trained model.
    
    Necessary parameters are in the global scope,
    loaded from config.json.

    Args: None (all paths in the global scope, loaded from config.json)
    Returns:
        y_pred (list): predictions for the test dataset
    """    #calculate summary statistics here
    #return value should be a list containing all summary statistics
    pass

def execution_time():
    #calculate timing of training.py and ingestion.py
    #return a list of 2 timing values in seconds
    pass

def outdated_packages_list():
    #get a list of 
    pass

if __name__ == '__main__':
    y_pred = model_predictions()
    dataframe_summary()
    missing_data()
    execution_time()
    outdated_packages_list()





    
