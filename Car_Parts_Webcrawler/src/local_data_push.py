from datetime import date
import os
from pathlib import Path

import pandas as pd

from src import local_data_pull as ld_pull


def csv_file_name(car_year: int, car_make: str, car_model: str, car_part: str) -> Path:
    """Creates a file name and file path based upon date, car year, car make, 
    car model, and car part to create a file path. 
    file name format: YYYY-MM-DD_car-year_car-make_car-mode_car-part
    
    Args: None
    
    Returns completed file path"""

    records_keeping_dir = ld_pull.get_top_level_directories().get("records_keeping")
    file_name = f"{date.today()}_{car_year}_{car_make}_{car_model}_{car_part}.csv"
    full_file_path = os.path.join(records_keeping_dir, file_name)
    return full_file_path

def save_csv_records(df: pd.DataFrame, csv_file_path: Path) -> None:
    """Takes a DataFrame and the csv_file_path then saves it 
    to records_keeping as file name from csv_file_path
    
    Args: df (pd.DataFrame) pandas dataframe to be saved. 
          csv_file_path (Path) full csv file path to write to_csv
          
    Returns: None. Writes file to file path"""
    
    df.to_csv(csv_file_path, index = False)