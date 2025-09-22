from datetime import date
import os
import json
from src import local_data_pull as ld_pull

def save_api_calls(call_count: int) -> None:
    """Save API Calls
    This function saves the API calls to the json file.

    Args:
        call_count, integer of how many calls have been made to dictionary.com

    Returns:
        None, updates JSON file with current call count
    """
    api_call_path = ld_pull.get_top_level_directories().get("record_keeping")
    api_record_path = os.path.join(api_call_path, "api_calls.json")

    with open(api_record_path, "w") as api_record_file:
        data = [{"api_calls": call_count, "date": date.today().isoformat()}]
        json.dump(data, api_record_file, indent=2)

def save_etymology_dict(updated_list: list) -> None:
    """Function to write the current list to the etymology_dict.json
    
    Args: updated list of new words and their information
    
    Returns: None, writes to the json file"""

    record_keeping_path = ld_pull.get_top_level_directories().get("record_keeping")
    etymology_file_path = os.path.join(record_keeping_path, "etymology_dict.json")
    
    with open(etymology_file_path, "w") as etymology_file:
        json.dump(updated_list, etymology_file, indent=2)
