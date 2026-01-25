#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
import pandas as pd

from src import helper

class Ingest_Data:

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def template_column_list(self) -> list:
        """Pulls list of column names from source_documents/HOR_Template.csv
        
        Args: None
        
        Returns: list of correct columns"""

        hor_template_path = os.path.join(helper.get_source_documents_directory(), "HOR_template.csv")
        hor_template = pd.read_csv(hor_template_path)
        return hor_template.columns.to_list()

    def eliminate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function to remove unneeded columns to fit criteria for columns. 
        Hopefully makes things a little bit simpler
        
        Args: df a pandas dataframe that is fed into the the function
        
        Returns: df with less columns to pass column test"""

        # Fetch the names for the template
        template_column_names = self.template_column_list()

        # Iterate through them and drop all unneeded ones
        for column in df.columns:
            if column not in template_column_names:
                df = df.drop(axis=1, columns=column)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(current_dir, "..", "source_documents", f"HORs.csv"))
        df.to_csv(csv_path, index=False)
        return df


    def test_file_columns(self, csv_columns: list, from_email: bool = False) -> None:
        """Checks the file columns of the given list against a list pulled from the hor_template.csv
        If there is no match, clears the downloads, emails a failure script, then
        raises a value error and exits the program
        
        Args: csv_columns a list of the csv columns to be tested against the template
        
        Returns: Value Error if columns do not match the template"""

        template_column_names = self.template_column_list()

        if sorted(template_column_names) != sorted(csv_columns):
            # Test if the file originated from an email
            if from_email:
                self.clear_downloads()
            raise ValueError(f"Incorrect Column names expected {template_column_names} and got {csv_columns}")

    def get_file_columns(self, hor_csv_path: Path = None) -> str:
        """Check file columns function. Relies upon hor_template.csv to check if columns in file match columns in delivered file. 
        If it does not, it clears downloads, emails the origin email and exits the program.
        
        Args: None
        
        Returns: path to current hor csv"""
        
        current_hor_csv_path = hor_csv_path
        current_hor_csv = pd.read_csv(hor_csv_path)
        reduced_columns_csv = self.eliminate_columns(current_hor_csv)
        current_hor_columns = reduced_columns_csv.columns.to_list()
        self.test_file_columns(csv_columns=current_hor_columns)

        return current_hor_csv_path

    def read_json_file(self, json_file_path: str) -> dict:
        """Function to read json file and return data as a dictionary. Used to reduce McCabe Score
        
        Args: json_file_path = string path leading to the json file
        
        Returns: Dictionary"""

        with open(json_file_path, 'r') as file_data:
            data = json.load(file_data)
            return data
        
    def mov_file(self, hor_csv_path: Path = None) -> Path:
        """Renames designated file to HORs.csv then moves to source_documents
        
        Args: None
        
        Returns: final csv path since all checks have been completed."""
        final_csv_path = os.path.abspath(os.path.join(helper.get_source_documents_directory(), "HORs.csv"))

        if hor_csv_path == None:
            # If no argument passed then check file columns from downloads
            new_hor_csv_path = self.get_file_columns()
            shutil.move(new_hor_csv_path, final_csv_path)            
        
        else:
            # If an argument is passed then check file columns from passed file
            new_hor_csv_path = self.get_file_columns(hor_csv_path=hor_csv_path)
            shutil.move(new_hor_csv_path, final_csv_path)
        
        return final_csv_path