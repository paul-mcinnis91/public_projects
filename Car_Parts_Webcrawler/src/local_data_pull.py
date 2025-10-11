import os

import pandas as pd

def get_top_level_directories() -> dict:
    """Returns dictionary of all top level directories in module.
    
    Args: None
    
    Returns: dictionary of all top level modules.
            Keys: 
                bin: bin path,
                geckodriver: geckodriver path
                src: src path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    child_dir_list = os.listdir(parent_dir)

    top_level_directories = {}
    top_level_directories["parent_directory"] = parent_dir
    
    for top_level_dir in child_dir_list:
        dir_path_test = os.path.join(parent_dir, top_level_dir)
        if os.path.isdir(dir_path_test):
            top_level_directories[top_level_dir] = dir_path_test
    
    return top_level_directories

def package_records_keeping() -> list:
    """Function to package the files and their file paths for 
    user_interactions.user_input_matches
    
    Args: None
    
    Returns: list of file paths"""

    records_keeping_dir = get_top_level_directories().get("records_keeping")
    file_list = [file for file in os.listdir(records_keeping_dir)]
    return file_list
    

def build_records_keeping_df() -> pd.DataFrame:
        """Draws upon ld_pull.package_records_keeping to get file information. 
        Parses out information to make a list of dictionaries.
        
        Args: None
        
        Returns pd.DataFrame of csv's available with columns for date, index, 
        make, model, year, part"""

        file_list = package_records_keeping()

        date_column = []
        year_column = []
        make_column = []
        model_column = []
        part_column = []
        file_path_column = []


        for file_info in file_list:
            file_name = os.path.split(file_info)[1]
            file_wo_ext = os.path.splitext(file_name)[0]
            date, year, make, model, part = file_wo_ext.split("_")
            date_column.append(date)
            year_column.append(year)
            make_column.append(make)
            model_column.append(model)
            part_column.append(part)
            file_path_column.append(file_info)
        

        dict_to_df = dict()
        dict_to_df["Query Date"] = date_column
        dict_to_df["Car Year"] = year_column
        dict_to_df["Car Make"] = make_column
        dict_to_df["Car Model"] = model_column
        dict_to_df["Car Part"] = part_column
        dict_to_df["File Path"] = file_path_column
        
        return pd.DataFrame(dict_to_df)