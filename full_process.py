"""This module runs the full monitoring
process, which is condensed in run_monitoring()
ans has the following steps:

- Check if there is new data; if so, continue
- Check if there is model or data drift; if so:
    - Re-train
    - Re-deploy
    - Run reporting for the re-deployed model 
    - Compute new score for the re-deployed model
    - Run diagnostics for the re-deployed model

After that, we can spin up the diagnostics server:

    $ python app.py

And that server can be accessed by external stakeholders;
as an example, api_calls.py shows how:

    $ python api_calls.py

Author: Mikel Sagardia
Date: 2023-02-20
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

 # "data/development", "data/production"
input_folder_path = os.path.join(os.getcwd(),
                                 config['input_folder_path'])
# "data/ingested/ingested_files.csv"
ingestion_record_path = os.path.join(os.getcwd(),
                                     config['prod_deployment_path'],
                                     config['compilation_record_filename'])
# "models/development/latest_score.csv"
score_path = os.path.join(os.getcwd(),
                          config['prod_deployment_path'],
                          config['score_filename'])
# "deployment/trained_model.pkl"
model_path = os.path.join(os.getcwd(),
                          config['prod_deployment_path'],
                          config['model_filename'])
# "data/ingested/final_data.csv"
dataset_csv_path = os.path.join(os.getcwd(),
                                config['output_folder_path'],
                                config['compiled_data_filename'])

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
    That occurs when the score from the deployed model
    is different (smaller) from the score from the model 
    that uses the newest ingested data.
    """
    # Get old score F1
    scores = pd.read_csv(score_path)
    f1_old = scores.iloc[-1,-1]
    # Score new model with new data
    f1 = scoring.score_model(model_path=model_path,
                             data_path=dataset_csv_path)
    # If new F1 score is better, there is model drift
    has_drift = False
    if f1_old < f1:
        has_drift = True
        
    return has_drift
    
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
            print("There is drift: re-training and re-deploying...")
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
            # and execute api_calls.run()
            # FIXME: That's not a very good idea, because
            # we would need to launch a separate 
            # web server (with app.py) to which we access from another
            # process (api_calls.py). Then, we'd need to
            # kill the web server again.
            # Instead, I think it's better start the server
            # manually:
            #   $ (shell 1) python app.py
            #   $ (shell 2) python api_calls.py
            print("New model replaced successfully!")
        else:
            print("No significant changes found; continuing with current model.")            
    else:
        print("No new data found; continuing with current model.")


if __name__ == "__main__":
    run_monitoring()
