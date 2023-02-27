This folder contains the monitoring databases which are set up by `db_setup.py`.

When `ingestion.py` and `scoring.py` are run, these files are generated/updated:

- `monitoring.sqlite`: database which stores all ingestion and scoring records.
- `ingestions.csv`: a dump of the `Ingestions` table from `monitoring.sqlite`.
- `scores.csv`: a dump of the `Scores` table from `monitoring.sqlite`.
