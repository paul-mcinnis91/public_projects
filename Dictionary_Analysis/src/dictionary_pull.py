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
            list with the response json, and the url
        """
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.college_key}"
        url_minus_key = url.replace(f"?key={self.college_key}", "")
        response = requests.get(url)
        self.call_count += 1
        return [response.json(), url_minus_key]
    
    def determine_known_unk(self, json_response: list) -> bool:
        """Function used to determine if the word is in the dictionary database or no.
        If no, returns false. Otherwise, true.

        Args: json_response from pull_dictionary

        Returns: bool
        """

        if isinstance(json_response[0][0], str):
            return False
        
        return True
        
        

    def etymology(self, json_response: list) -> str:
        """Etymology
        This function returns the etymology of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            Etymology string
        """
        try:
            json_response[0].keys()
            et_key = json_response[0].get("et")
            et_key_0 = et_key[0]
            return et_key_0[0]
        except (AttributeError, KeyError):
            return "Unknown"


    def word_date(self, json_response: list) -> str:
        """Word Date
        This function returns the origination date of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            Date info string
        """
       
        json_0_idx: dict = json_response[0]
        origination_date = json_0_idx.get("date")

        if isinstance(origination_date, None):
            return "Unknown"
        
        return origination_date
    
    def package_et_date(self, json_response: list, index: int, word: str) -> dict:
        """Function that takes the json response and strips out the needed parts for packaging.
        Once packing is complete, another function will write this to etymology_dict.json"""

        # Example package: {"Index": 0, 
        #                   "Word": "a", 
        #                   "Etymology": "Unknown", 
        #                   "Origination Date": "before 12th century{ds||1|a|}"
        #                   }

        response_dict = {}
        response_dict["Index"] = index
        response_dict["Word"] = word
        response_dict["Etymology"] = self.etymology(json_response)
        response_dict["Origination Date"] = self.word_date(json_response)

        return response_dict


    