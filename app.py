"""This is a diagnostics API which external stakeholders
can use to request information about the status of the model:

- /predict: given a dataset, predict the churn
- /scoring: given a test dataset, score the model
- /summarystats: given a dataset, compute its colum statistics
- /diagnostics/timing: measure time to ingest and train
- /diagnostics/dependencies: dependency status
- /diagnostics: redirects to /diagnostics/timing

The config.json file contains important parameters
used in the API.

To run this app:

    $ python app.py

Then, on another terminal / browser:

    $ curl http://localhost:8000/prediction?filename=data/test/test_data.csv
    $ curl http://localhost:8000/scoring?filename=data/test/test_data.csv
    $ curl http://localhost:8000/summarystats?filename=data/ingested/final_data.csv
    $ curl http://localhost:8000/diagnostics/timing
    $ curl http://localhost:8000/diagnostics/dependencies
    $ curl http://localhost:8000/diagnostics

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
import json
import pandas as pd
#import numpy as np
#import pickle
from flask import Flask, request, redirect, url_for # session, jsonify

from scoring import score_model
from diagnostics import (model_predictions,
                         dataframe_summary,
                         execution_time,
                         outdated_packages_list)

with open('config.json','r') as f:
    config = json.load(f) 

# The Flask secret key is used to sign session cookies
# for protection against cookie data tampering. 
# It's very important that an attacker doesn't know the value of this secret key.
# Ways to solve that:
# 1. Define FLASK_SECRET_KEY in env and import it with os.environ.get('FLASK_SECRET_KEY')
# 2. Define FLASK_SECRET_KEY as a secret in our CI environment
# 3. Place a secret key in the development config, which gets committed to the repo. 
#       In production, use a production config (which is never committed to the repo),
#       with a unique secret key.
app = Flask(__name__)
app.secret_key = config['flask_secret_key']

# "data/ingested/final_data.csv"
dataset_csv_path = os.path.join(os.getcwd(),
                                config['output_folder_path'],
                                config['compiled_data_filename'])
# "models/production/trained_model.pkl"
model_path = os.path.join(os.getcwd(),
                          config['prod_deployment_path'],
                          config['model_filename'])
 # "models/production/latest_score.csv"
score_path = os.path.join(os.getcwd(),
                          config['prod_deployment_path'],
                          config['score_filename'])
# "data/test/test_data.csv"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename'])
features = config['features'] # ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
target = config['target'] # 'exited'

# It's a nice practice to return the reponse as 
# (reponse, http_status)
HTTP_STATUS_200 = 200

@app.route("/prediction") # methods=['POST','OPTIONS']
def predict():
    """Predict in batch given a path to a dataset, e.g.,
    data/test/test_data.csv
    
    Example call:
        http://localhost:8000/prediction?filename=data/test/test_data.csv
    """
    response = "Prediction not tested."
    filename = request.args.get('filename')
    try:
        y_pred, _ = model_predictions(data_path=filename, # test_data_path
                                      model_path=model_path,
                                      features=features,
                                      target=target)
        response = str(y_pred)
    except FileNotFoundError as err:
        response = "File not found."
    
    return response, HTTP_STATUS_200

@app.route("/scoring") # methods=['GET','OPTIONS']
def scoring():        
    """Predict in batch given a path to a dataset, e.g.,
    data/test/test_data.csv, and compute F1 score.
    
    Example call:
        http://localhost:8000/scoring?filename=data/test/test_data.csv
    """
    response = "Prediction not tested."
    filename = request.args.get('filename')
    try:
        f1 = score_model(model_path=model_path,
                         data_path=filename,
                         score_path=score_path,
                         features=features,
                         target=target)
        response = str(f1)
    except FileNotFoundError as err:
        response = "File not found."
    
    return response, HTTP_STATUS_200

@app.route("/summarystats") # methods=['GET','OPTIONS']
def stats():
    """Given a dataset, compute its summary stats, i.e.,
    for each column/feature: mean, median, std. dev., NAs.
    
    Example call:
        http://localhost:8000/summarystats?filename=data/ingested/final_data.csv
    """
    response = "Prediction not tested."
    filename = request.args.get('filename')
    try:
        statistics = dataframe_summary(data_path=filename, # dataset_csv_path
                                       features=features)
        response = pd.DataFrame(statistics).to_html()
    except FileNotFoundError as err:
        response = "File not found."
    
    return response, HTTP_STATUS_200

@app.route("/diagnostics/timing") # methods=['GET','OPTIONS']
def timing():  
    """Check the time necessary for ingestion and training.
    
    Example call:
        http://localhost:8000/diagnostics/timing
    """
    response = "Prediction not tested."
    try:
        timing = execution_time()
        response = str({"ingestion": timing[0], "training": timing[1]})
    except FileNotFoundError as err:
        response = "File not found."
    
    return response, HTTP_STATUS_200

@app.route("/diagnostics/dependencies") # methods=['GET','OPTIONS']
def dependencies():  
    """Check the dependencies.
    
    Example call:
        http://localhost:8000/diagnostics/dependencies
    """
    response = "Prediction not tested."
    try:
        packages = outdated_packages_list()
        response = pd.DataFrame(packages).to_html()
    except FileNotFoundError as err:
        response = "File not found."
    
    return response, HTTP_STATUS_200

@app.route("/diagnostics") # methods=['GET','OPTIONS']
def diagnostics():
    """Redirect to "/diagnostics/timing"""
    # url_for() expects either the page/view function
    return redirect(url_for("timing"))

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
