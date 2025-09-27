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

def save_clean_et_dict(cleaned_list: list) -> None:
    """Function to save the cleaned list into a different file. This way we can compare the old
    with the new and ensure we are maintaining the correct data
    
    Args: cleaned_list (list): list that has been filtered and cleansed by the data_cleanse object
    
    Returns: None. Saves the data to cleaned_dict.json"""

    record_keeping_path = ld_pull.get_top_level_directories().get("record_keeping")
    cleaned_file_path = os.path.join(record_keeping_path, "cleaned_dict.json")
    
    with open(cleaned_file_path, "w") as cleaned_file:
        json.dump(cleaned_list, cleaned_file, indent=2)

def save_dirty_list(dirty_list: list) -> None:
    """Function to take all the words that had unknown etmologies and origination dates and dump
        them into the unknown_words.txt
        
        Args: dirty_list (list) takes the filtered list of dirty_words, and writes it to 
        unknown_words.txt
        
        Returns: None"""
    
    record_keeping_path = ld_pull.get_top_level_directories().get("record_keeping")
    unknown_words_path = os.path.join(record_keeping_path, "unknown_words.txt")
    formatted_dirty_words = "".join([dirty_word + "\n" for dirty_word in dirty_list])
    

    with open(unknown_words_path, "w") as unknown_words_file:
        unknown_words_file.write(formatted_dirty_words)
        
    