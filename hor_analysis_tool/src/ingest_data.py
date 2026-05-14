import json
import os
from pathlib import Path
import sys
import pandas as pd

from src import helper

class Ingest_Data:

    def __init__(self, hor_csv_path: Path):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.hor_csv_path = hor_csv_path
        self.template_columns = self._template_column_list()

    def _template_column_list(self) -> list:
        """Pulls list of column names from source_documents/HOR_Template.csv
        
        Args: None
        
        Returns: list of correct columns"""

        hor_template_path = os.path.join(helper.get_source_documents_directory(), "HOR_template.csv")
        hor_template = pd.read_csv(hor_template_path)
        return hor_template.columns.to_list()


    def _test_file_columns(self, csv_columns: list, from_email: bool = False) -> None:
        """Checks the file columns of the given list against a list pulled from the hor_template.csv
        If there is no match exits the program
        
        Args: csv_columns a list of the csv columns to be tested against the template
        
        Returns: Value Error if columns do not match the template"""

        template_column_names = self.template_columns

        if sorted(template_column_names) != sorted(csv_columns):
            # Test if the file originated from an email
            sys.exit(f"Incorrect Column names expected {template_column_names} and got {csv_columns}")

    def validate_file(self, hor_csv_path: Path = None) -> str:
        """Check file columns function. Relies upon hor_template.csv to check if columns in file match columns in delivered file. 
        If it does not, it clears downloads, emails the origin email and exits the program.
        
        Args: None
        
        Returns: path to current hor csv"""
        
        current_hor_csv_path = hor_csv_path
        current_hor_csv = pd.read_csv(hor_csv_path)
        current_hor_columns = current_hor_csv.columns.to_list()
        self._test_file_columns(csv_columns=current_hor_columns)

        return current_hor_csv_path

   

