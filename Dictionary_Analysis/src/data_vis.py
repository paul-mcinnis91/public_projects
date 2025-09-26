import collections
import sys
import matplotlib.pyplot as plt
import pandas as pd
from src import local_data_pull as ld_pull


class Data_Manipulation:

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

        ety_pairs = [(language, entry.get("Origination Date")) for entry in self.ety_list for language in entry.get("Etymology")]
        known_pairs = [(language, entry.get("Origination Date")) for entry in self.all_known_list for language in entry.get("Etymology")]

        ety_counter = collections.Counter(ety_pairs)
        known_counter = collections.Counter(known_pairs)
        
        ety_result = [(language, date, count) for (language, date), count in ety_counter.items()]
        known_result = [(language, date, count) for (language, date), count in known_counter.items()]

        return (ety_result, known_result)
    

class Data_Visualizations(Data_Manipulation):
    
    def __init__(self):
        super().__init__()

    def _dates_language_vis(self, user_func) -> None:
        """Special use case function for the visualization of the Origin Dates by Language count
        since the ouput of that function (count_dates_ets) is a list of tuples
        
        Args: Function to get the return from self.count_dates_ets
        
        Returns: None, visualizes the bar or pie chart (undecided) for the user"""

        language_all = user_func()[0]
        language_known = user_func()[1]

        df_all = pd.DataFrame(language_all, columns = ["Language", "Date", "Count"])
        df_known = pd.DataFrame(language_known, columns = ["Language", "Date", "Count"])

        df_all["Date"] = pd.to_datetime(df_all["Date"])
        df_known["Date"] = pd.to_datetime(df_known["Date"])

        pivot_all = df_all.pivot(index="Date", columns="Language", values="Count").fillna(0)
        pivot_known = df_known.pivot(index="Date", columns="Language", values="Count").fillna(0)

        pivot_all.plot(marker="o")
        plt.title("All Languages: Languages over Time")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.legend(title="Language")
        plt.show()

        pivot_known.plot(marker="o")
        plt.title("Known Languages: Languages over Time")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.legend(title="Language")
        plt.show()




    def visualiziations(self, user_selection: str) -> None:
        """Gives you three options to pick a visualization draws that from an internal dictionary.
        
        The internal dictionary will return the inherited function with the correct information to 
        create the visualization.
        
        Args: user_selection (str) a string that the user puts in to pick the visualization they want
        Options = ['Language Origin Pie Chart', 
                    'Origin Dates Bar Chart', 
                    'Origin Dates by Language Bar Chart']
                    
        Returns: list information for language_all"""

        language_all = user_selection()[0]
        language_known = user_selection()[1]


        function_dictionary = {"Languages Origin Pie Chart": self.count_ets,
                               "Origin Dates Bar Chart": self.count_dates,
                               "Origin Dates by Language Bar Chart": self.count_dates_ets}

        user_function = function_dictionary.get(user_selection)

        if isinstance(user_function, type(None)):
            sys.exit("Incorrect key entered in visualizations function")

        if user_function.__name__ != "count_dates_ets":
            language_all = list(user_function()[0].keys())
            language_all_count = list(user_function()[0].values())

            language_known = list(user_function()[1].keys())
            language_known_count = list(user_function()[1].values())
        
        else:
            self._dates_language_vis(user_function)
        
        
        
        if "Pie" in user_selection:
    
            plt.figure(1)
            plt.pie(language_all_count, labels = language_all, autopct='%1.1f%%')
            plt.title("All " +  user_selection)

            plt.figure(2)
            plt.pie(language_known_count, labels = language_known, autopct='%1.1f%%')
            plt.title("Known " +  user_selection)

            plt.show()
        
        plt.figure(1)
        plt.bar(x = language_all, height = language_all_count)
        plt.title("All " + user_selection)

        plt.figure(2)
        plt.bar(x = language_known, height = language_known_count, )
        plt.title("Known " +  user_selection)
        
        plt.show()

