"""This module 
"""
import os
import json
import pandas as pd

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f)

# "data/ingested/final_data.csv"
dataset_csv_path = os.path.join(os.getcwd(),
                                config['output_folder_path'],
                                config['compiled_data_filename'])
 # "data/development", "data/production"
input_folder_path = os.path.join(os.getcwd(),
                                 config['input_folder_path'])
# "data/ingested/ingested_files.csv"
ingestion_record_path = os.path.join(os.getcwd(),
                                     config['output_folder_path'],
                                     config['compilation_record_filename'])
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

def check_ingested_data():
    """Check that all the files from config.input_folder_path
    have a record in data/ingested/ingested_files.csv.
    If not, ingest new data and return True, else False.
    """
    # Load records of ingested files
    records = pd.read_csv(ingestion_record_path)
        
    # Get files in source directory
    filenames = os.listdir(input_folder_path)

    # Check if all files in source directory
    # have a record
    all_in = False
    for each_filename in filenames:
        if each_filename.endswith(".csv"):
            filepath = os.path.join(input_folder_path,
                                    each_filename)
            if not filepath in records['filepath'].to_list():
                break
        all_in = True
    
    if not all_in:
        ingestion.merge_multiple_data()

    return not all_in

def check_model_drift():
    """Check whether there is model drift:
    
    """
    #check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
    pass

def check_data_drift():
    """Check whether there is data drift:
    That occurs when the distributions of the column values
    change considerably.
    """
    # TODO: This needs to be implemented yet
    # However, the most important function is check_model_drift()
    # because the only relevant data drifts are those which
    # cause a model drift!
    # One way of implementing this is with a T-Test,
    # diagnostics.dataframe_summary() provides with all the information
    # to compute that.
    return False

def run_monitoring():
    """Run monitoring:
    - Check if there is new data; if so, continue
    - Check if there is model or data drift; if so:
        - Re-train
        - Re-deploy
        - Run reporting for the re-deployed model 
        - Compute new score for the re-deployed model
        - Run diagnostics for the re-deployed model
    """
    if check_ingested_data():
        model_drift = False
        data_drift = False
        model_drift = check_model_drift()
        data_drift = check_data_drift()
        if model_drift or data_drift:
            # Re-Train
            training.train_model()
            # Re-Deploy
            deployment.store_model_into_pickle()
            # Run Reporting
            reporting.score_model()
            # Compute New Score
            _ = scoring.score_model()
            # Run Diagnostics
            diagnostics.run_diagnostics()
            # Spin up diagnostics server
            # NO
        else:
            print("No significant changes found; continuing with current model.")            
    else:
        print("No new data found; continuing with current model.")

if __name__ == "__main__":
    run_monitoring()
