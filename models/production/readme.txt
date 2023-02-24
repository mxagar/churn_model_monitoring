This folder is populated during production, i.e., when the datasets used for training are taken from `data/source`.

After `training.py`is run, this folder should contain:

- `trained_model.pkl`
- `latest_score.csv`: score records of the trained model

After `reporting.py` is run, this folder should contain `confusion_matrix.png`.

After `api_calls.py` is run, this folder should contain `api_returns.txt`; that file contain the responses of all API endpoint calls.