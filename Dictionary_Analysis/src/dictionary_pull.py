import re
import requests
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
        self.call_count = ld_pull.get_user_credentials().get("api_calls")
        
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
        so we can actually get the etymology. If et key is not present adds et key
        to all dictionaries. Will be called upon in filter_for_len
        
        Args: json_response(dict) the json_response from the dictionary resposne
        
        Returns list of filtered items with the 'et' key"""

        et_filtered = list(filter(lambda json_ob: "et" in json_ob.keys(), json_response))
        if len(et_filtered) == 0:
            et_added = [{**json_ob, 'et': "Unknown"} for json_ob in json_response]
            return et_added
        
        return et_filtered
    
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

    def package_et_date(self, json_response: dict, index: int, word: str) -> dict:
        """Function that takes the json response and strips out the needed parts for packaging.
        Once packing is complete, another function will write this to etymology_dict.json"""

        # Example package: {"Index": 0, 
        #                   "Word": "a", 
        #                   "Etymology": "Unknown", 
        #                   "Origination Date": "before 12th century{ds||1|a|}"
        #                   }
        
        etymology = json_response.get("et")
        orig_date = json_response.get("date")

        if isinstance(orig_date, list):
            orig_date = orig_date[1]


        if isinstance(orig_date, type(None)):
            orig_date = "Unknown"

        filtered_etymology = self._filter_special_characters(str(etymology))
        filtered_orig_date = self._filter_special_characters(str(orig_date))


        response_dict = {}
        response_dict["Index"] = index
        response_dict["Word"] = word
        response_dict["Etymology"] = filtered_etymology
        response_dict["Origination Date"] = filtered_orig_date

        return response_dict


    