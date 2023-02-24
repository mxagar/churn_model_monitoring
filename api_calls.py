"""This module tests the API by calling all its
endpoints:

http://localhost:8000/prediction?filename=data/test/test_data.csv
http://localhost:8000/scoring
http://localhost:8000/scoring?filename=data/test/test_data.csv
http://localhost:8000/summarystats
http://localhost:8000/summarystats?filename=data/ingested/final_data.csv
http://localhost:8000/diagnostics/timing
http://localhost:8000/diagnostics/dependencies
http://localhost:8000/diagnostics

A file is saved to disk with all the responses:
api_call_path: models/development/api_returns.txt

Author: Mikel Sagardia
Date: 2023-02-20
"""
import os
import json
import requests
import pandas as pd

with open('config.json','r') as f:
    config = json.load(f) 

# "data/test/test_data.csv"
test_data_path = os.path.join(os.getcwd(),
                              config['test_data_path'],
                              config['test_data_filename'])
# "models/development/api_returns.txt"
api_call_path = os.path.join(os.getcwd(),
                             config['output_model_path'],
                             config['api_call_filename'])

def run():
    """Main function in which all API calls
    are run and where their responses are saved to file.
    """
    # Specify base URL that resolves to our workspace
    URL = "http://127.0.0.1:8000"
    # Lists of all responses and endpoints
    endpoints = []
    responses = []

    # Create endpoint calls
    endpoints.append(URL + "/prediction?filename=" + test_data_path) # data/test/test_data.csv
    endpoints.append(URL + "/scoring")
    endpoints.append(URL + "/summarystats") # HTML table
    endpoints.append(URL + "/diagnostics/timing")
    endpoints.append(URL + "/diagnostics/dependencies") # HTML table

    # Call endpoints and collect responses
    for i, endpoint in enumerate(endpoints):
        # GET method, extract content, convert to string
        response = requests.get(endpoint).content.decode("utf-8") 
        if i == 2 or i == 4:
            responses.append(pd.read_html(response)[0].drop("Unnamed: 0", axis=1).to_string())
        else:
            responses.append(response)
        # Display
        print("\n")
        print(endpoint)
        print(responses[-1])

    # Save responses to file
    with open(api_call_path, 'w') as f:
        f.write("--- API Calls Report ---\n")
        for i, endpoint in enumerate(endpoints):
            f.write("\n" + endpoint + "\n")
            f.write(responses[i] + "\n")

if __name__ == "__main__":
    run()