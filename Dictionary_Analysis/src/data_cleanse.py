import re
from src import local_data_pull as ld_pull


class Data_Cleanse:
    """Data Cleanse class. Relies upon ld_pull and push gather and clean data.
    Conducts several different types of data cleansing to make sure data can be sorted and used correctly"""
    def __init__(self):
        self.lang_list: list = self._cleaned_lang_list()
        self.all_words_lang: list = [word for sentence in self.lang_list for word in sentence.split()]


    def _cleaned_lang_list(self) -> list:
        """Function to reduce amount of calls made out to language.txt
        
        Args: None
        
        Returns list of cleaned language list"""
        dirty_ets = ld_pull.get_word_lang_list("language")
        cleaned_ets = [language.split(" (")[0] for language in dirty_ets]
        return cleaned_ets
    
    def _test_capital_in_et(self, ety_str: str) -> list:
        """Function to test if there are any capital letters in the etymology string. 
        Dictionary.com did a good job of capitalizing proper nouns.
        
        Args: ety_str (str) the unpacked etymology string
        
        Returns: list of all words that are capitalized"""

        return re.findall(r'\b[A-Z][a-zA-Z]*\b', ety_str)

    def _reduce_et(self, etymology: str) -> list:
        """Function to reduce etymology string to list of single words that can be queried later
        Checks if the the words are in the language list and then returns the ones that are
        
        Args: etymology(string) the actual etymology being fed into the function.
        
        Returns: list of where the word is from (language of origin)"""

        capital_words: list = self._test_capital_in_et(etymology)

        et_options = [word for word in capital_words if word in self.all_words_lang]
        
        return et_options
    
    def _clean_date(self, date_str: str) -> int:
        """The purpose of this function is to pull the date_str and determine what year the word
        came from. Once that is determined, to return that word as an integer
        This will be one of the more difficult functions to deal with.
        
        Args: date_str (str) pulled from the 'date' key in the etymology_dict
        
        Returns: Integer format of the 'date' key"""

      
        numbers_only = re.findall(r"\d+", date_str)
        new_date = numbers_only[0]
        if "century" in date_str:
            new_date = numbers_only[0] + "00"
        
        return int(new_date)

    def _test_unk(self, date_et_str: str) -> bool:
        """Function to test if the date or et is equal to unknown. If the word is something 
        other than 'Unknown' returns true.
        
        Args: date_et_str (str) the date or etymology string being test
        
        Returns: bool"""

        if date_et_str == "Unknown":
            return False
        
        return True
    
    def _filter_unk(self, etymology_list: list) -> list:
        """Filters out all json objects where the etymology AND origination dates are listed 'Unknown'. 
        
        Args: etymology_list (list[dict]) list of dictionaries from within the cleaned_list function
        
        Returns: filterd_list (list[dict]) list of the same dictioanaries but filtered out unknowns"""

        filtered_list = list(filter(lambda json_ob: 
                                        self._test_unk(json_ob.get("Origination Date")) == True
                                        and self._test_unk(json_ob.get("Etymology") == True), 
                                        etymology_list))

        return filtered_list
    
    def _get_correct_languages(self, etymology_str: str) -> list:
        """Designed to pull out word modifieres from the etymology_list
        
        Args: etymology_str (str) string of etymology words that will be turned into a list
                                    of capital letters then filtered from there.
        
        Returns: available_modifiers (list) list of available modifiers"""

        available_modifiers = []
        etymology_list = self._reduce_et(etymology_str)
        et_list_len = len(etymology_list) - 1
        for idx in range(et_list_len):
            if idx <= et_list_len - 2:
                new_word = " ".join(etymology_list[idx: idx +2])
                
            elif idx <= et_list_len -1:
                new_word = " ".join(etymology_list[idx: idx +1])

            available_modifiers.append(new_word)

        correct_languages = [modifier for modifier in available_modifiers if modifier in self.lang_list]
        if len(correct_languages) == 0:
            return etymology_list
        return correct_languages


        
    def dirty_list(self, all_word_list: list, filtered_list: list) -> list:
        """Takes the all_word_list and returns every item that is not in the filtered_list
        
        Args: all_word_list (list) List of Dictionaries pulled from etymology_dict.json
              filtered_list (list) List of Dictionaries that have known etymology or known orig dates
        
        Returns: unknown_words (list) all words that have unknown etymology and dates"""
        filter_list_words = [word.get("Word") for word in filtered_list]
        unknown_words = [word for word in all_word_list if word not in filter_list_words]
        return unknown_words

    def cleaned_list(self, etymology_list: list) -> list:
        """Takes the etymology_list that is passed into it and runs the previous functions to cleanse it
        
        Args: etymology_list (list[dict]) list of dictionaries from etymology_dict.json
        
        Returns cleansed_list (list[dict]) list of dictioanries with cleaned data"""

        filtered_list = self._filter_unk(etymology_list)
        cleansed_list = []
        for json_ob in filtered_list:
            dirty_etymology = json_ob.get("Etymology")
            dirty_orig_date = json_ob.get("Origination Date")
            
            cleaned_et = self._get_correct_languages(dirty_etymology)
            cleaned_orig_date = self._clean_date(dirty_orig_date)

            json_ob["Origination Date"] = cleaned_orig_date
            json_ob["Etymology"] = cleaned_et
            
            cleansed_list.append(json_ob)
        
        return cleansed_list

        





