"""This module is in charge of running diagnostics
of several components in the system:

- Model predictions
- Training dataset statistics, i.e., column means, NAs, etc.
- Timing for ingestion and training
- Dependencies (expected versions vs. actual)

The config.json file parametrizes the necessary paths
and filenames.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import timeit
import os
from subprocess import PIPE, Popen
import json
import pandas as pd
#import numpy as np

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

def cmdline(command):
    """Auxiliary function which returns the output
    of a CLI subprocess in which we can use pipes.
    Source:
    https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    """
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return str(process.communicate()[0])

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
    """Compute the summary statistics of the dataset
    used for training; for each feature, we get:
    
    - Mean
    - Median
    - Standard deviation
    - Number of missing rows/entries (NAs)
    - Percent of missing rows/entries (NAs)    

    Args: None (all paths in the global scope, loaded from config.json)
    Returns:
        statistics (dict): dictionary with summary statistics
    """
    # Load dataset
    df = pd.read_csv(dataset_csv_path)

    # Compute summary statistics
    means = []
    medians = []
    std_devs = []
    num_nas = []
    pcnt_nas = []
    for feat in features:
        means.append(df[feat].mean())
        medians.append(df[feat].median())
        std_devs.append(df[feat].std())
        num_nas.append(df[feat].isna().sum())
        pcnt_nas.append(100.0*df[feat].isna().sum()/df.shape[0])

    # Pack results to a dictionary
    statistics = {"feature": features,
                   "mean": means,
                   "median": medians,
                   "std_dev": std_devs,
                   "num_na": num_nas,
                   "pcnt_na": pcnt_nas}

    return statistics

def execution_time():
    """Compute the time required by
    ingestion.py and training.py
    
    Args: None
    Return:
        timing (list): time in seconds for ingestion and training
    """
    start_time = timeit.default_timer()
    os.system('python ingestion.py')
    timing_ingestion = timeit.default_timer() - start_time

    start_time = timeit.default_timer()
    os.system('python training.py')
    timing_training = timeit.default_timer() - start_time

    return [timing_ingestion, timing_training]

def outdated_packages_list():
    """Create a list of all packages listed in requirements.txt
    and for each detect the expected and actual version.

    Returns:
        package (dict): dictionary with package version (actual & expected)
    """
    # Load requirements.txt
    with open('requirements.txt',mode='r') as f:
        requirements = f.readlines()

    # Loop all lines in requirements.txt: packages
    package_names = []
    expected_versions = []
    actual_versions = []
    for req in requirements:
        req_split = req.split("==")
        # Get package name
        package_name = req_split[0]
        if not package_name.isspace():
            # Get package's expected version
            expected_version = "-"
            if (len(req_split) > 1):
                # Version specified
                expected_version = req_split[1][:-1] # take number and remove \n
            # Get package's current version
            #pip_info = subprocess.check_output(["python", "-m", "pip", "show", package_name, "|", "grep", "Version"])
            pip_info = cmdline(f"python -m pip show {package_name} | grep Version")
            actual_version = pip_info.split(" ")[1][:-3] # take number and remove \n'
            # Store 
            package_names.append(package_name)
            expected_versions.append(expected_version)
            actual_versions.append(actual_version)

    # Pack results
    packages = {"package": package_names,
                "expected_version": expected_versions,
                "actual_version": actual_versions}

    return packages

if __name__ == '__main__':

    y_pred = model_predictions()

    statistics = dataframe_summary()
    statistics_df = pd.DataFrame(statistics)

    timing = execution_time()

    packages = outdated_packages_list()
    packages_df = pd.DataFrame(packages)
