# A Dynamic Risk Assessment System: Monitoring of a Customer Churn Model

This project contains a dynamic risk assessment system in which a customer churn model is monitored after a simulated deployment.

*Customer churn* refers to the clients that have a high probability of halting the use of the services provided by a company, a.k.a. attrition risk. This is a common business problem faced by all companies; a related key principle behind it is that it's easier to keep a customer than getting a new one. Thus, the goal is to predict churn and a to avoid it.

I took the [starter code](https://video.udacity-data.com/topher/2021/March/60412fe6_starter-file/starter-file.zip) for this project from the [Udacity Machine Learning DevOps Engineer Nanodegree](https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821) and modified it to the present form, which deviates significantly from the original version.

The focus of this project doesn't lie so much on the data processing or modeling, but on the techniques and technologies used for model/pipeline **monitoring after deployment**; in fact, dummy datasets are used instead of realistic ones. A list of the most important MLOps monitoring methods and tools used is the following:

- [ ] A
- [ ] A
- [ ] A

- [A Dynamic Risk Assessment System: Monitoring of a Customer Churn Model](#a-dynamic-risk-assessment-system-monitoring-of-a-customer-churn-model)
  - [Dataset](#dataset)
  - [How to Use This Project](#how-to-use-this-project)
    - [Installing Dependencies for Custom Environments](#installing-dependencies-for-custom-environments)
  - [Notes on Theory](#notes-on-theory)
  - [Notes on the Implemented Analysis and Modeling](#notes-on-the-implemented-analysis-and-modeling)
    - [Summary of Contents](#summary-of-contents)
  - [Results and Conclusions](#results-and-conclusions)
  - [Next Steps, Improvements](#next-steps-improvements)
  - [References and Links](#references-and-links)
  - [Authorship](#authorship)


## Dataset

The dataset is composed of 5 CSV files, with 5 columns each, distributed as follows:

```
data
├── ingested/           # Ingested data folder (populated when run)
│   └── ...
├── development         # Data used during development
│   ├── dataset1.csv    # Shape: (17, 5)
│   └── dataset2.csv    # Shape: (19, 5)
├── source              # Data for re-training
│   ├── dataset3.csv    # Shape: (11, 5)
│   └── dataset4.csv    # Shape: (15, 5)
└── test                # Data for model testing
    └── test_data.csv   # Shape: (5, 5)
```

The files contain fabricated information of hypothetical corporations and, as shown, they consist of less than 20 entries/rows each. The 5 common columns are the following:

- `corporation`: fictional name of the customer company (hashed name)
- `lastmonth_activity`: number of services/goods provided last month
- `lastyear_activity`: number of services/goods provided last year
- `number_of_employees`: number of employees at the customer company
- `exited`: **target**, whether the customer company ceased to buy services/goods.

In summary, the dataset consists of 3 useful numerical features and a binary classification is done, which predicts customer company churn.

## How to Use This Project

The directory of the project consists of the following files:

```
.
├── Instructions.md         # Summary of instructions by Udacity
├── README.md               # This file
├── api_calls.py            # Calls to the API
├── app.py                  # API endpoints
├── assets/                 # Images and additional files
│   └── ...
├── conda.yaml              # Development environment dependencies
├── config.json             # Configuration parameters for scripts
├── data/                   # Dataset(s)
│   └── ...
├── deployment.py           # It deploys a trained model
├── diagnostics.py          # Model and data diagnostics
├── full_process.py         # It checks whether re-deploy needed
├── ingestion.py            # It ingests new data
├── models/                 # Training artifacts (dev and prod)
│   └── ...
├── reporting.py            # Reports about model metrics
├── requirements.txt        # Deployment dependencies
├── scoring.py              # Model scoring
├── training.py             # Model training, artifacts generated
└── wsgi.py                 # API deployment
```

Additionally, after the execution, new files are created:

```
...
```

You can run the notebook at leas in two ways:

1. In a custom environment, e.g., locally or on a container. To that end, you can create a [conda](https://docs.conda.io/en/latest/) environment and install the [dependencies](#installing-dependencies-for-custom-environments) as explained below.
2. In Google Colab. For that, simply click on the following link:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mxagar/airbnb_data_analysis/blob/master/00_AirBnB_DataAnalysis_Initial_Tests.ipynb)


### Installing Dependencies for Custom Environments

If you'd like to control where the notebook runs, you need to create a custom environment and install the required dependencies. A quick recipe which sets everything up with [conda](https://docs.conda.io/en/latest/) is the following:

```bash
# Create environment with YAML, incl. packages
conda env create -f conda.yaml
conda activate env-name
# Or
conda create --name env-name pip
condat install <package>

# Install pip dependencies
pip install requirements.txt

# Track any changes and versions you have
conda env export > conda_.yaml
pip list --format=freeze > requirements_.txt
```


## Monitoring Implementation

As mentioned in the introduction, this mini-project focuses on **monitoring techniques**. Monitoring is essential in production after having deployed a machine learning model, because it helps address inevitable issues that will appear in our system, such as:

- Data drift: sooner or later, the distribution of data features that arrive to the model will change as compared to the original training dataset; we need to detect that to re-train and re-deploy the inference pipeline.
- Data integrity: some features might be missing or corrupt; we should detect and process them.
- Model accuracy might decrease with time, e.g., because the business context changes (more customers leave than usual because of the global economic situation); we should detect that to re-train the model.
- New component versions might destabilize the system; we should detect and fix those dependency inconsistencies.
- etc.

To fix all those issues, monitoring is applied in 5 aspects:

1. Data Ingestion
2. Training, Scoring, Deploying
3. Diagnostics
4. Reporting
5. Process Automation

### 1. Data Ingestion

The script [`ingestion.py`](./ingestion.py) is responsible for merging data from different sources. Additionally, a record of source information is stored in order to backtrace the origin of the values.

As the rest of the scripts, [`ingestion.py`](./ingestion.py) relies on [`config.json`](./config.json), which defines all the parameters (i.e., filenames, paths/URLs, etc.).

Produced outputs:

- `data/ingested/final_data.csv`: merged dataset.
- `data/ingested/ingested_files.csv`: dataset origin info related to the merge (path, entries, timestamp).

### 2. Training, Scoring, Deploying

After loading all the necessary parameters from [`config.json`](./config.json), the following three files train the inference pipeline (model), evaluate its performance (i.e., score it on a test dataset) and deploy it to the production location (sub-tasks listed):

- [`training.py`](./training.py):
  - Read merged dataset: `data/ingested/final_data.csv`
  - Define and train a logistic regression model
  - Save the model pickle: `models/development/trained_model.pkl`
- [`scoring.py`](./scoring.py):
  - Load the saved model pickle: `models/development/trained_model.pkl`
  - Load the test dataset: `data/test/test_data.csv`
  - Compute the F1 score of the model on the test dataset
  - Persist score records to file: `models/development/latest_score.csv`
- [`deployment.py`](./deployment.py):
  - Copy the following files from the development/practice folders to the production folder `models/production`:
    - The trained model: `models/development/trained_model.pkl`
    - The records of the ingested data files used for training: `data/ingested/ingested_files.csv`
    - The records of the model scores: `models/development/latest_score.csv`

### 3. Diagnostics

The script [`diagnostics.py`](./diagnostics.py) is responsible tracking dataset properties (to prevent data drift) and model predictions (to prevent model drift). Additionally, it measures operational aspects (timings, dependencies) to prevent anomalies. All in all it:

- Performs model predictions with a test dataset: `data/test/test_data.csv`.
- Provides with statistics of the training dataset, i.e., column means, medians, std. devs., NAs (count and percentage).
- Computes the timing for for the `ingestion.py` and `training.py` scripts.
- Provides information on dependencies: expected versions vs. actual per package; the `requirements.txt` file is used.

### 4. Reporting

Reporting is a accomplished with three scripts:

- [`reporting.py`](./reporting.py)
- [`app.py`](./app.py)
- [`api_calls.py`](./api_calls.py)

The file [`reporting.py`](./reporting.py) uses the `model_prediction()` function from `diagnostics.py` to predict the classes from `data/test/test_data.csv` and generate a confusion matrix, which is saved to `models/development/confusion_matrix.png`.

If we fun the file [`app.py`](./app.py), it creates and serves an API based on Flask with the following endpoints, which can be used from another terminal session or with the browser:

```bash
# Predict in batch given a path to a dataset, e.g., data/test/test_data.csv
curl "http://localhost:8000/prediction?filename=data/test/test_data.csv"

# Predict in batch given a path to a dataset and compute F1 score; 
# if no filename passed, data/test/test_data.csv is used.
curl "http://localhost:8000/scoring"

# Given a dataset, compute its summary stats, i.e.,
# for each column/feature: mean, median, std. dev., NAs;
# if no filename passed, data/ingested/final_data.csv is used.
# Note: HTML table is returned.
curl "http://localhost:8000/summarystats"

# Check the time necessary for ingestion and training.
curl "http://localhost:8000/diagnostics/timing"

# Check the dependencies.
# Note: HTML table is returned.
curl "http://localhost:8000/diagnostics/dependencies"

# Redirect to '/diagnostics/timing'.
curl "http://localhost:8000/diagnostics"
```

In [`app.py`](./app.py), the functions from `diagnostics.py` are used to compute the responses.

Finally, the file [`api_calls.py`](./api_calls.py) uses all those API endpoints and writes their responses to the file `models/development/api_returns.txt`.

As always, any necessary parameters (i.e., paths, filenames, etc.) are taken from `config.json`.

### 5. Process Automation


## Results and Conclusions

## Next Steps, Improvements

- [ ] Generate PDF reports which aggregate all outcomes (plots, summary statistics, etc.); check: [reportlab](https://www.reportlab.com/).
- [ ] Store time trends: timestamp the reported results and store them (e.g., NAs, latency, etc.).
- [ ] Store datasets and records in SQL databases, e.g., with [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/).

## References and Links

- A
- B
- C
- Link
- Link

## Authorship

Mikel Sagardia, 2022.  
No guarantees.

If you find this repository useful, you're free to use it, but please link back to the original source.