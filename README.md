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

```
data
├── practice            # Practice data
│   ├── dataset1.csv
│   └── dataset2.csv
├── source              # Data for training
│   ├── dataset3.csv
│   └── dataset4.csv
└── test
    └── test_data.csv
```

## How to Use This Project

The directory of the project consists of the following files:

```
.
├── Instructions.md         # Summary of instructions by Udacity
├── README.md               # This file
├── api_calls.py
├── app.py
├── conda.yaml
├── config.json
├── data/                   # Dataset(s)
├── deployment.py
├── diagnostics.py
├── full_process.py
├── ingestion.py
├── models/                 # Training artifacts
├── production_deployment/  # Final deployed models
├── reporting.py
├── requirements.txt
├── scoring.py
├── training.py
└── wsgi.py
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

List of most important dependencies:

- A
- B

## Notes on Theory

## Notes on the Implemented Analysis and Modeling

### Summary of Contents

- [ ] A
- [ ] B

## Results and Conclusions

## Next Steps, Improvements

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