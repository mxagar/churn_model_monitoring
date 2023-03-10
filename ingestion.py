"""This module is in charge of ingesting data
from different sources to create a single dataset.

The config.json file parametrizes the input/output
paths for the data.

Author: Mikel Sagardia
Date: 2023-02-20
"""
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from db_setup import Database

# Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

# "data/development", "data/production"
input_folder_path = config['input_folder_path']
# "data/ingested"
output_folder_path = config['output_folder_path']
# "final_data.csv"
compiled_data_filename = config['compiled_data_filename']
# "ingested_files.txt"
compilation_record_filename = config['compilation_record_filename']
# ['corporation', 'lastmonth_activity', 'lastyear_activity', 'number_of_employees', 'exited']
dataset_columns = config['dataset_columns']

def merge_multiple_data():
    """Check for datasets, compile them together, 
    and write to an output file/database.
    Additionally, a record of all the merged
    dataset files is written.
    
    Output filenames can be found in config.json and are
    persisted to config.output_folder_path:
    
    - config.compiled_data_filename
    - config.compilation_record_filename
    
    Args: None (all global variables from config.json)
    Returns: None (compiled dataset persisted to file)
    """
    # Instantiate empty dataframe: 'corporation', 'lastmonth_activity', 'lastyear_activity', 'number_of_employees', 'exited'
    final_df = pd.DataFrame(columns=dataset_columns)
    
    # Files in directory
    path = os.path.join(os.getcwd(), input_folder_path)
    filenames = os.listdir(path)
    
    # Instantiate records array
    records = []

    # Merge all dataset files    
    for each_filename in filenames:
        if each_filename.endswith(".csv"):
            filepath = os.path.join(os.getcwd(),
                                    input_folder_path,
                                    each_filename)
            current_df = pd.read_csv(filepath)
            # Store record
            records.append([filepath, len(current_df), datetime.now()])
            # Concatenate dataframes + reset index!
            final_df = pd.concat([final_df, current_df], axis=0)
            final_df = final_df.reset_index(drop=True)

    # Now, we can do some cleaning...
    final_df.drop_duplicates().reset_index(drop=True)

    # Persist aggregated dataframe
    filepath = os.path.join(os.getcwd(),
                            output_folder_path,
                            compiled_data_filename)
    final_df.to_csv(filepath, sep=',', header=True, index=False)
    
    # Create TXT/CSV with record info
    filepath = os.path.join(os.getcwd(),
                            output_folder_path,
                            compilation_record_filename)
    with open(filepath, 'w') as f:
        f.write("filepath,num_entries,timestamp\n")
        for record in records:
            for i, element in enumerate(record):
                f.write(str(element))
                if i < len(record)-1:
                    f.write(",")
                else:
                    f.write("\n")
    
    # EXTRA: Persist to sqlite database
    # FIXME: we should not instantiate the database every ingestion
    # but rather pass it to the ingestion process...
    db = Database()
    for record in records:
        db.insert_ingestion({"filepath": record[0], "num_entries": record[1], "timestamp": record[2]})
    # Check: convert to CSV
    ingestions = db.convert_ingestions_to_df()
    ingestions.to_csv('db/ingestions.csv', sep=',', header=True, index=False)
    db.close()

if __name__ == '__main__':
    merge_multiple_data()
