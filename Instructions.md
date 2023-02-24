# Monitoring of a Customer Churn Model: Instructions

This file contains the summary of the instructions provided by Udacity.

The project starter file can be downloaded from here: [starter-file.zip](https://video.udacity-data.com/topher/2021/March/60412fe6_starter-file/starter-file.zip).

Overview of steps:

> 1. Data ingestion. Automatically check a database for new data that can be used for model training. Compile all training data to a training dataset and save it to persistent storage. Write metrics related to the completed data ingestion tasks to persistent storage.
> 2. Training, scoring, and deploying. Write scripts that train an ML model that predicts attrition risk, and score the model. Write the model and the scoring metrics to persistent storage.
> 3. Diagnostics. Determine and save summary statistics related to a dataset. Time the performance of model training and scoring scripts. Check for dependency changes and package updates.
> 4. Reporting. Automatically generate plots and documents that report on model metrics. Provide an API endpoint that can return model predictions and metrics.
> 5. Process Automation. Create a script and cron job that automatically run all previous steps at regular intervals.

Submission: ZIP with project + reports from step 4.

Udacity encourages to use the Linux Virtual machine accessed via their web interface; the starter code should be downloaded into `/home/workspace`. Even though the files persist between sessions, shell sessions are lost; additionally, the workspace closes automatically after 30 idle minutes.

## Project Steps

### 1. Data Ingestion

The file `ingestion.py` needs to be created, which:

- Loads `config.json`
- Reads all datasets from the folders specified in the config
- Merges all datasets
- Removes duplicates
- Persists merged dataset to specified path
- Saves a record of all the merged data files

### 2. Training, Scoring, Deploying

Three files need to be created, which carry out the tasks explained in the following; note that all the parameters required for the tasks should be in the `config.json` file, which needs to be loaded in every module:

- `training.py`:
  - Read merged dataset
  - Define and train a logistic regression model
  - Save the model pickle
- `scoring.py`:
  - Load the saved model pickle
  - Load the test dataset
  - Compute the F1 score of the model on the test dataset
  - Persist score records to file
- `deployment.py`:
  - Copy from the development/practice folders to the production folder the following files:
    - The trained model
    - The records of the ingested data files used for training
    - The records of the model scores

### 3. Diagnostics

The file `diagnostics.py` needs to be created, which:

- Performs model predictions with a test dataset
- Provides with statistics of the training dataset, i.e., column means, medians, std. devs., NAs (count and percentage).
- Computes the timing for for the ingestion and training scripts
- Provides information on dependencies: expected versions vs. actual per package

### 4. Reporting

Three files need to be created: `reporting.py`, `app.py` and `api_calls.py`.

The file `reporting.py` should create a confusion matrix image using the functionalities from `diagnostics.py`.

The file `app.py` should create and serve an API with the following endpoints, that call the functionalities in `diagnostics.py`:

```bash
# Predict in batch given a path to a dataset, e.g., data/test/test_data.csv
curl "http://localhost:8000/prediction?filename=data/test/test_data.csv"

# Predict in batch given a path to a dataset and compute F1 score; 
# if no filename passed, data/test/test_data.csv is used.
curl "http://localhost:8000/scoring"

# Given a dataset, compute its summary stats, i.e.,
# for each column/feature: mean, median, std. dev., NAs;
# if no filename passed, data/ingested/final_data.csv is used.
curl "http://localhost:8000/summarystats"

# Check the time necessary for ingestion and training.
curl "http://localhost:8000/diagnostics/timing"

# Check the dependencies.
curl "http://localhost:8000/diagnostics/dependencies"
```

Finally, the file `api_calls.py` should use all those API endpoints and write to a file their responses.

As always, any necessary parameters (i.e., paths, filenames, etc.) should be taken from `config.json`.

### 5. Process Automation

First:
  
- Change `input_folder_path` in `config.json` from `data/development` to `data/production`.
- Change `output_model_path` in `config.json` from `models/development` to `models/production`.

Second, create the file `full_process.py`, which performs the following actions:

- Check if there is new data; if so, continue
- Check if there is model or data drift; if so:
  - Re-train
  - Re-deploy
  - Run reporting for the re-deployed model 
  - Compute new score for the re-deployed model
  - Run diagnostics for the re-deployed model



## Submission

Submit a ZIP file with the following content:

- `training.py`
- `scoring.py`
- `deployment.py`
- `ingestion.py`
- `diagnostics.py`
- `reporting.py`
- `app.py`
- `apicalls.py`
- `fullprocess.py`
- `finaldata.csv` contains all the data that has been read from the practice data folder
- `ingestedfiles.txt` that contains a list of filenames of the data that have been read from the practice data folder
- `trainedmodel.pkl` contains a trained model using practice data
- `latestcore.txt` that stores the F1 score from the practice model
- `confusionmatrix.png` and `condusionmatrix2.png` output by the reporting.py
- `apireturns.txt` and `apireturns2.txt` that contain the combined outputs of each of the API endpoints
- `crontab` file

### Rubric Summary

All files need to be finished, the project needs to be working.

- Data ingestion: `finaldata.csv` and `ingestedfiles.txt` files generated.
- Training, scoring, deployment
  - Model pickle persisted
  - `latestscore.txt` generated
  - `production_deployment` populated
- Diagnostics
  - Timing for ingestion and training
  - Column summary statistics: mean, median, mode
  - Data integrity: NA percentage
  - Check dependency versions
- Reporting API
  - Scoring endpoint
  - Summary statistics endpoint
  - Diagnostics endpoint
  - Model predictions endpoint
  - Confusion matrix
  - `api_calls.py` uses all endpoints and generates `api_returns.txt`
- Process automation: `full_process.py`, `deployment.py`
  - Check whether re-training and re-deployment necessary and perform them
  - Cron job