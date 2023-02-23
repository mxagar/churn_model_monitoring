"""This module is in charge of evaluating the trained
model with a test dataset. The results are used
to generate a confusion matrix plot which is saved
to disk.

The config.json file parametrizes the input/output
paths and filenames for all artifacts.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
import json
#import pickle
#import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

from diagnostics import model_predictions

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
# 'models/development/confusion_matrix.png'
plot_path = os.path.join(os.getcwd(),
                         config['output_model_path'],
                         config['plot_filename'])
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'

def score_model():
    """Run a prediction with the trained model and
    the test dataset. Then, compute the confusion matrix
    and save it to disk.
    
    Necessary parameters in global scope after loading
    config.json.
    
    Args: None (in global scope)
    Returns: None (plot saved to disk)
    """
    # Run prediction
    y_pred, y_test = model_predictions(data_path=test_data_path,
                                       model_path=model_path,
                                       features=features,
                                       target=target)
    
    # Plot and save to disk
    plt.figure(figsize=(10,10))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.savefig(plot_path, dpi=300, transparent=False, bbox_inches='tight')


if __name__ == '__main__':
    score_model()
