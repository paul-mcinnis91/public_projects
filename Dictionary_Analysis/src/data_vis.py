import collections
from src import local_data_pull as ld_pull


class Data_Visualization:

    def __init__(self):
        self.ety_list: list = ld_pull.get_cleaned_words()
        self.all_known_list: list = list(filter(lambda json_ob : len(json_ob.get("Etymology"))> 0, self.ety_list))


    def count_ets(self) -> tuple:
        """Takes self._all_known_list and self.ety_list and checks date and etymology counts
        
        Args: None
        
        Returns (tuple) with two counter objects with the ety_counter and known_counter counters"""
        ety_values = [et_values for et_dict in self.ety_list for et_values in et_dict.get('Etymology')]
        known_et_values = [known_value for known_dict in self.all_known_list for known_value in known_dict.get('Etymology')]
        ety_counter = collections.Counter(ety_values)
        known_counter = collections.Counter(known_et_values)

        return (ety_counter, known_counter)
    
    def count_dates(self) -> tuple:
        """Takes self._all_known_list and self.ety_list and checks date and etymology counts
        
        Args: None
        
        Returns (tuple) with two counter objects with the date_counter and known_date_counter counters"""
        date_values = [et_dict.get("Origination Date") for et_dict in self.ety_list]
        known_date_values = [known_dict.get("Origination Date") for known_dict in self.ety_list]
        date_counter = collections.Counter(date_values)
        known_date_counter = collections.Counter(known_date_values)

        return (date_counter, known_date_counter)
    
    def count_dates_ets(self) -> tuple:
        """Function pull when an etymology poppped up with a certain date then add it to a counter.
        
        Args: None
        
        Returns tuple of counters that count the language and dates and group them together and count them"""

        ety_pairs = [(word, entry.get("Origination Date")) for entry in self.ety_list for word in entry.get("Etymology")]
        known_pairs = [(word, entry.get("Origination Date")) for entry in self.all_known_list for word in entry.get("Etymology")]

        ety_counter = collections.Counter(ety_pairs)
        known_counter = collections.Counter(known_pairs)
        
        ety_result = [(word, date, count) for (word, date), count in ety_counter.items()]
        known_result = [(word, date, count) for (word, date), count in known_counter.items()]

        return (ety_result, known_result)
    
