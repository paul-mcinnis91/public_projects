import collections
from src import local_data_pull as ld_pull


class Data_Visualization:

    def __init__(self):
        self.ety_list: list = ld_pull.get_cleaned_words()
        self.all_known_list: list = list(filter(lambda json_ob : len(json_ob.get("Etymology"))> 0, self.ety_list))


    def count_ets_dates(self) -> tuple:
        """Takes self._all_known_list and self.ety_list and checks date and etymology counts
        
        Args: None
        
        Returns key_et_counters (tuple) two counter objects with the ety_list and all_known_list counters"""
        ety_keys = [et_key for et_dict in self.ety_list for et_key in et_dict.values()]
        known_keys = [known_key for known_dict in self.all_known_list for known_key in known_dict.values()]
        ety_counter = collections.Counter(ety_keys)
        known_counter = collections.Counter(known_keys)

        return (ety_counter, known_counter)

