"""This module is in charge of managing the monitoring
database, which currently stores all ingestion and scoring
records in db/monitoring.sqlite, in two tables: Ingestions
and Scores.

A class Database is defined here which handles all necessary
functionalities to interface with the SQLite database.

The files ingestion.py and scoring.py make use of the Database.

The config.json file parametrizes the input/output
paths for the data.

Author: Mikel Sagardia
Date: 2023-02-27
"""
import os
import sqlalchemy as db
from sqlalchemy.sql import func
import pandas as pd

DATABASE_FILENAME = "sqlite:///db/monitoring.sqlite"

class Database():
    def __init__(self, filename=DATABASE_FILENAME):
        """Constructor.
        
        Args:
            filename (str): filename of the database, default: DATABASE_FILENAME"""
        self.engine = None
        self.conn = None
        self.metadata = None
        # Tables
        self.ingestions = None
        self.scores = None
        self.tables = (self.ingestions, self.scores)
        # Initialize
        self.setup(filename=filename)

    def setup(self, filename=DATABASE_FILENAME):
        """Initialization, run in the constructor.
        
        Args:
            filename (str): filename of the database, default: DATABASE_FILENAME"""
        # Check if database file exists
        db_exists = os.path.isfile(filename)
        
        # Connect
        self.engine = db.create_engine(filename)
        self.conn = self.engine.connect()
        self.engine = self.engine.execution_options(autocommit=True)
        self.metadata = db.MetaData()

        # Define tables: Ingestions, Scores
        # Ingestions, CSV: filepath, num_entries, timestamp
        self.ingestions = db.Table('Ingestions',
                        self.metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('filepath', db.String(255), nullable=False),
                        db.Column('num_entries', db.Integer(), nullable=False),
                        db.Column('timestamp', db.DateTime(timezone=True), server_default=func.now()),
                        sqlite_autoincrement=True
                        )
        # Scores, CSV: model_version, timestamp, score_type, value
        self.scores = db.Table('Scores',
                        self.metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('model_version', db.String(255), nullable=False),
                        db.Column('timestamp', db.DateTime(timezone=True), server_default=func.now()),
                        db.Column('score_type', db.String(255), default="F1"),
                        db.Column('value', db.Numeric(), nullable=False),
                        sqlite_autoincrement=True
                        )
        
        # Write file to disk, if not present
        if not db_exists:
            self.metadata.create_all(self.engine)
                
    def insert(self, values, table):
        """Insert the values into the table.
        Both must be consistent.
        
        Args:
            values (dict): dictionary representation of a row.
            table (sqlalchemy.Table): table.
        """
        query = db.insert(table)
        # values: dict: col_name: value, ...
        values_list = [values]
        _ = self.conn.execute(query, values_list)
        self.conn.commit() # necessary for version >=2.0
    
    def insert_ingestion(self, values):
        """Insert row to ingestions.
        
        Args:
            values (dict): keys: filepath, num_entries, timestamp
        """
        self.insert(values, self.ingestions)
    
    
    def insert_score(self, values):
        """Insert row to scores.

        Args:
            values (dict): keys: model_version, timestamp, score_type, value
        """
        self.insert(values, self.scores)
    
    def to_df(self, table):
        """Convert a table into
        a dataframe.

        Args:
            table (sqlalchemy.Table): table object.
        Returns:
            df (pd.DataFrame): table dataframe.
        """
        query = table.select()
        output = self.conn.execute(query)
        results = output.fetchall()
        df = pd.DataFrame(results)
        #df.columns = results[0].keys()
        output.close()
        
        return df
    
    def convert_ingestions_to_df(self):
        """Convert ingestions table into
        a dataframe.

        Returns:
            df (pd.DataFrame): ingestions dataframe.
        """
        df = self.to_df(self.ingestions)
        df.columns = ['id', 'filepath', 'num_entries', 'timestamp']
        
        return df

    def convert_scores_to_df(self):
        """Convert scores table into
        a dataframe.

        Returns:
            df (pd.DataFrame): scores dataframe.
        """
        df = self.to_df(self.scores)
        df.columns = ['id', 'model_version', 'timestamp', 'score_type', 'value']

        return df

    def close(self):
        self.conn.close()
        self.engine.dispose()
