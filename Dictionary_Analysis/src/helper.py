from datetime import date
import json
from json import JSONDecodeError
import os


def get_top_level_directories() -> dict:
    """Returns dictionary of all top level directories in module.
    
    Args: None
    
    Returns: dictionary of all top level modules.
            Keys: 
                bin: bin path,
                keys: keys path
                record_keeping: record_keeping path
                setup: setup path
                src: src path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    child_dir_list = os.listdir(parent_dir)

    top_level_directories = {}

    for top_level_dir in child_dir_list:
        dir_path_test = os.path.join(parent_dir, top_level_dir)
        if os.path.isdir(dir_path_test):
            top_level_directories[top_level_dir] = dir_path_test
    
    return top_level_directories

def get_user_credentials() -> dict:
    """Gets user credentials from keys directory. Also pulls current api count from the record keeping
    directory. Combines all the information into a single dictionary for later querying
    
    Args: None
    
    Returns: dict with 3 keys; 
                api_calls: call count to avoid going over 1000 a day
                api_date: last date the count was upated
                api_key: key to acccess the database"""
    
    keys_path = get_top_level_directories().get("keys")
    records_path = get_top_level_directories().get("record_keeping")
    api_record_path = os.path.join(records_path, "api_calls.json")
    
    api_path = os.path.abspath(os.path.join(keys_path, "api.txt"))

    credentials_dict = {}


    with open(api_record_path, "r") as api_record_file:

        data: list = json.load(api_record_file)
        data_dict: dict = data[0]

        if data_dict.get("date") != date.today().isoformat():
            save_api_calls(0)
            data_dict["api_calls"] = 0

        credentials_dict["api_calls"] = data_dict.get("api_calls")
        credentials_dict["api_date"] = data_dict.get("date")

    with open(api_path) as api_info:
        api_text: str = api_info.read()
        credentials_dict["api_key"] = api_text
    
    return credentials_dict

def get_current_words() -> dict:
    """Pulls current etymology dictionary so the program knows what word to start from for today
    
    Args: None
    
    Returns: Dictionary with current words that have been recorded"""

    records_path = get_top_level_directories().get("records_keeping")
    etymology_dict_json = os.path.abspath(os.path.join(records_path, "etymology_dict.json"))
    with open(etymology_dict_json) as etymology_json:
        etymology_dict: dict = json.load(etymology_json)
        return etymology_dict
        

def save_api_calls(call_count: int):
    """Save API Calls
    This function saves the API calls to the json file.

    Args:
        call_count, integer of how many calls have been made to dictionary.com

    Returns:
        None, updates JSON file with current call count
    """
    api_call_path = get_top_level_directories().get("record_keeping")
    api_record_path = os.path.join(api_call_path, "api_calls.json")

    with open(api_record_path, "w") as api_record_file:
        data = [{"api_calls": call_count, "date": date.today().isoformat()}]
        json.dump(data, api_record_file, indent=2)
   


if __name__ == "__main__":
    save_api_calls(5)
    x = get_user_credentials().get("api_calls")
    print(x)
    
    