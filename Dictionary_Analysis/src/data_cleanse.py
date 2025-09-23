from src import local_data_pull as ld_pull


class Data_Cleanse:
    """Data Cleanse class. Relies upon ld_pull and push gather and clean data.
    Conducts several different types of data cleansing to make sure data can be sorted and used correctly"""
    def __init__(self):
        self.etymology_dict: list = ld_pull.get_current_words()
    

    def reduce_et(self, etymology: str) -> list:
        """Function to reduce etymology string to list of single words that can be queried later
        
        Args: etymology(string) the actual etymology being fed into the function.
        
        Returns: list of where the word is from (language of origin)"""

        possible_ets = ld_pull.get_word_lang_list("language")
        cleaned_ets = [language.split(" (")[0] for language in possible_ets]
        current_et_split = etymology.split(" ")
        et_options = [word for word in current_et_split if word in cleaned_ets]
        
        return et_options
    
    def clean_date(self, date_str: str) -> int:
        """The purpose of this function is to pull the date_str and determine what year the word
        came from. Once that is determined, to return that word as an integer
        This will be one of the more difficult functions to deal with.
        
        Args: date_str (str) pulled from the 'date' key in the etymology_dict
        
        Returns: Integer format of the 'date' key"""

        



