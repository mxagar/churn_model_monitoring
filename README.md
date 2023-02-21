# A Dynamic Risk Assessment System: Monitoring of a Customer Churn Model

The project contains a dynamic risk assessment system in which a customer churn model is monitored after a simulated deployment.

*Customer churn* refers to customers that have high probability of leaving the services of a company, a.k.a. attrition risk. This is a common business problem faced by all companies; a related key principle behind it is that it's easier to keep a customer than getting a new one.

[starter-file.zip](https://video.udacity-data.com/topher/2021/March/60412fe6_starter-file/starter-file.zip)

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

## How to Use This Project

The directory of the project consists of the following files:

```
.
├── Instructions.md           # Original challenge instructions
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