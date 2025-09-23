from datetime import date
import os
import json
from src import local_data_push as ld_push


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
            ld_push.save_api_calls(0)
            data_dict["api_calls"] = 0

        credentials_dict["api_calls"] = data_dict.get("api_calls")
        credentials_dict["api_date"] = data_dict.get("date")

    with open(api_path) as api_info:
        api_text: str = api_info.read()
        credentials_dict["api_key"] = api_text
    
    return credentials_dict


def get_current_words() -> list:
    """Pulls current etymology dictionary so the program knows what word to start from for today
    
    Args: None
    
    Returns: Dictionary with current words that have been recorded"""

    records_path = get_top_level_directories().get("record_keeping")
    etymology_dict_json = os.path.abspath(os.path.join(records_path, "etymology_dict.json"))
    with open(etymology_dict_json, "r") as etymology_json:
        string_json = etymology_json.read()
        etymology_dict_list: list = json.loads(string_json)

        if len(etymology_dict_list) == 0:
            return []
        
        return etymology_dict_list

def get_word_lang_list(list_choice: str) -> list:
    """Opens words_alpha.txt, executes read_lines, and returns the list
    
    args: list_choice (str) what list [words_alpha, language] is the end user asking for.
    
    Returns: word_list (list) list of all words from a github repo 
            found here: https://github.com/dwyl/english-words
            
            or
            
            language_list (list) list of all languages from a github repo 
            found here: https://github.com/umpirsky/language-list"""

    records_path = get_top_level_directories().get("record_keeping")
    
    path_dictionary = {}

    words_alpha_path = os.path.join(records_path, "words_alpha.txt")
    language_path = os.path.join(records_path, "language.txt")

    path_dictionary["words_alpha"] = words_alpha_path
    path_dictionary["language"] = language_path 

    
    with open(path_dictionary.get(list_choice)) as list_data:
        return list_data.readlines()

def get_current_index() -> int:
        """Current Index
        This function returns the current index of the word list from the etymology_dict.json file.

        Args:
            None

        Returns:
            Integer of current index
        """
        word_list = get_current_words()
        last_item: dict = word_list[-1]
        return last_item.get("Index")
          