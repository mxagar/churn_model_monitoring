# A Dynamic Risk Assessment System: Monitoring of a Customer Churn Model

This project contains a dynamic risk assessment system in which a customer churn model is monitored after a simulated deployment.

*Customer churn* refers to the clients that have a high probability of halting the use of the services provided by a company, a.k.a. attrition risk. This is a common business problem faced by all companies; a related key principle behind it is that it's easier to keep a customer than getting a new one. Thus, the goal is to predict churn and a to avoid it.

I took the [starter code](https://video.udacity-data.com/topher/2021/March/60412fe6_starter-file/starter-file.zip) for this project from the [Udacity Machine Learning DevOps Engineer Nanodegree](https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821) and modified it to the present form, which deviates significantly from the original version.

The focus of this project doesn't lie so much on the data processing or modeling, but on the techniques and technologies used for model/pipeline **monitoring after deployment**; in fact, dummy datasets are used instead of realistic ones. A list of the most important MLOps methods and tools used is the following:

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
├── practice            # Practice data
│   ├── dataset1.csv    # Shape: (17, 5)
│   └── dataset2.csv    # Shape: (19, 5)
├── source              # Data for training
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
├── models/                 # Training artifacts
│   └── ...
├── production_deployment/  # Final deployed models
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

### 1. Data Ingestion


### 2. Training, Scoring, Deploying


### 3. Diagnostics


### 4. Reporting


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