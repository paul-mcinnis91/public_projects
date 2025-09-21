import requests
from datetime import date
from src import local_data_pull as ld_pull

class dictionary_pull:
    """Dictionary Pull Class
    This class is used to pull the etymology of words from the dictionaryapi.com API.
    It is used to create a dictionary of words and their etymologies.

    The Constructor builds the API keys and sets the current API calls to the value in the json file.
    It also sets the today's date and registers the save_api_calls function to be called when the program is closed.

    At Exit, it saves the API calls to the json file.

    Args:
        None

    Returns:
        None
    """
    def __init__(self):
        self.college_key = ld_pull.get_user_credentials().get("api_key")
        self.today_date = date.today().strftime("%Y-%m-%d")
        self.call_count = ld_pull.get_user_credentials().get("api_calls")
        self.last_date = ld_pull.get_user_credentials().get("api_date")
        
    def pull_dictionary(self, word) -> list:
        """Pull Dictionary
        This function pulls the dictionary from the dictionaryapi.com API.

        Args:
            word (str): The word to pull the dictionary for.

        Returns:
            None
        """
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.college_key}"
        response = requests.get(url)
        self.call_count += 1
        return [response.json(), url]

    def etymology(self, json_response: list) -> str:
        """Etymology
        This function returns the etymology of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            None
        """
        try:
            json_response[0].keys()
        except (AttributeError, KeyError):
            return "Unknown"


    def word_date(self, json_response: list) -> str:
        """Word Date
        This function returns the origination date of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            None
        """
        try:
            json_response[0].keys()
        except AttributeError:
            return "Unknown"

        json_0_idx: dict = json_response[0]

        origination_date = json_0_idx.get("date")

        if origination_date.isdigit():
            return int(origination_date)
        elif isinstance(origination_date, None):
            return "Unknown"
        
        return origination_date
      
    
    