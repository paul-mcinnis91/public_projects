import re
import requests
from datetime import date
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push

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
        
    def pull_dictionary(self, word) -> dict:
        """Pull Dictionary
        This function pulls the dictionary from the dictionaryapi.com API.

        Args:
            word (str): The word to pull the dictionary for.

        Returns:
            response json
        """
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.college_key}"
        response = requests.get(url)
        self.call_count += 1
        ld_push.save_api_calls(self.call_count)
        return response.json()
    
    def _filter_special_characters(self, character_string: str) -> str:
        """Takes a string input and strips all non alphanumeric characters from it.
        Will be called on by word_date and etymology functions
        
        Args: character_string(str) string to be filtered
        
        Returns: String with only numbers and letters"""

        return re.sub(r'[^a-zA-Z0-9\s]', '', character_string)

    
    def _filter_for_et(self, json_response: list) -> list:
        """Takes json response and filters for items that contain the 'et' key 
        so we can actually get the etymology. Will be called upon in filter_for_len
        
        Args: json_response(dict) the json_response from the dictionary resposne
        
        Returns list of filtered items with the 'et' key"""

        return list(filter(lambda json_ob: "et" in json_ob.keys(), json_response))
    
    def filter_for_len(self, json_response: list) -> list:
        """Reduces the json_response to one item to reduce processing time. 
        
        Args: json_response (list) the json_response from dictionary.com
        
        Returns: filtered list with just one item"""

        et_only_response = self._filter_for_et(json_response)
        if len(et_only_response) > 0:
            return et_only_response[0]
    
    def determine_known_unk(self, json_response: dict) -> bool:
        """Function used to determine if the word is in the dictionary database or no.
        If no, returns false. Otherwise, true.

        Args: json_response from pull_dictionary

        Returns: bool
        """

        if isinstance(json_response[0], str):
            return False
        
        return True


    def _etymology(self, filtered_json: dict) -> str:
        """Etymology
        This function returns the etymology of a word from the json response.
        Will be called on in package_et_date.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            Etymology string
        """
        try:
            
            et_key = filtered_json.get("et")
            et_key_0 = et_key[0]
            return self._filter_special_characters(et_key_0[1])
        except (AttributeError, KeyError):
            return "Unknown"


    def _word_date(self, filtered_json: dict) -> str:
        """Word Date
        This function returns the origination date of a word from the json response.
        Will be called on in package_et_date.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            Date info string
        """
       
        try:
            origination_date = filtered_json.get("date")

        except AttributeError:
            return "Unknown"

        if isinstance(origination_date, type(None)):
            return "Unknown"
        
        return self._filter_special_characters(origination_date)
    
    def package_et_date(self, json_response: dict, index: int, word: str) -> dict:
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
        response_dict["Etymology"] = self._etymology(json_response)
        response_dict["Origination Date"] = self._word_date(json_response)

        return response_dict


    