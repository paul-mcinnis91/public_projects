import json
import os
import sys
import getpass

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)


def get_current_dir() -> str:
    """Returns current directory file is running in.
    
    Args: None
    
    Returns: current directory file is being run in."""
    return os.path.dirname(os.path.abspath(__file__))

def get_user_credentials() -> dict:
    """Gets user credentials from keys directory. Also pulls current api count from the record keeping
    directory. Combines all the information into a single dictionary for later querying
    
    Args: None
    
    Returns: dict with 3 keys; 
                api_calls: call count to avoid going over 1000 a day
                api_date: last date the count was upated
                api_key: key to acccess the database"""
    
    current_dir = get_current_dir()
    keys_path = os.path.abspath(os.path.join(current_dir, "..", "keys"))
    records_path = os.path.abspath(os.path.join(current_dir, "..", "record_keeping"))
    api_calls_path_json = os.path.abspath(os.path.join(records_path, "api_calls.json"))
    

    api_path = os.path.abspath(os.path.join(keys_path, "api.txt"))

    credentials_dict = {}

    with open(api_calls_path_json) as api_calls_info:
        api_calls_dict: dict = json.load(api_calls_info)
        credentials_dict["api_calls"] = api_calls_dict.get("api_calls")
        credentials_dict["api_date"] = api_calls_dict.get("date")

    with open(api_path) as api_info:
        api_text: str = api_info.read()
        credentials_dict["api_key"] = api_text
    
    return credentials_dict

def get_current_words() -> dict:
    """Pulls current etymology dictionary so the program knows what word to start from for today
    
    Args: None
    
    Returns: Dictionary with current words that have been recorded"""
    current_dir = get_current_dir()
    records_path = os.path.abspath(os.path.join(current_dir, "..", "record_keeping"))
    etymology_dict_json = os.path.abspath(os.path.join(records_path, "etymology_dict.json"))
    with open(etymology_dict_json) as etymology_json:
        etymology_dict: dict = json.load(etymology_json)
        

    def save_api_calls(self):
        """Save API Calls
        This function saves the API calls to the json file.

        Args:
            None

        Returns:
            None
        """
        file_path = get_user_credentials().get('api_calls')

        with open(file_path, "w") as file:
            try:
                data = [{"api_calls": self.call_count, "date": self.today_date}]
                json.dump(data, file, indent=2)
            except TypeError:
                data = [{"api_calls": 0, "date": {self.today_date}}]
                json.dump(data, file, indent=2)