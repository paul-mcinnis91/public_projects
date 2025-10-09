import sys
import pandas as pd

from src import local_data_pull as ld_pull

class User_Interface:
    def __init__(self):
        self.df = None

    def user_input_matches(self, matches_dict: dict) -> str:
        """Function to have the user pick from a list of matches and returns the number they
        selected corresponding to the part
        
        Args: matches_dict (dict) dictionary of links with the highest match value
        
        Returns: key that will unlock the full URL to get to the parts"""

        if len(matches_dict) == 1:
            max_key = max(matches_dict, key=matches_dict.get)
            return matches_dict[max_key]

        display_dict = {}
        for idx, key_str in enumerate(matches_dict):
            display_dict[idx] = key_str

        for key, value in display_dict.items():
            print(f"{key} -- {value}")
        user_part_choice = input("Select your part by the number next to it. If your part is not present, type quit ").lower()

        if user_part_choice[0] == 'q':
            sys.exit("No part selected")
        
        try: 
            int_key = int(user_part_choice)
            str_key = display_dict[int_key]
            return matches_dict[str_key]
        
        except ValueError:
            sys.exit("Invalid user input")
    
    def create_user_matches(self, user_matches: list) -> None:
        """Function  to intake the user_matches list and creates a pandas Dataframe 
        so that the user can manipulate their returned data without making more requests to 
        outside sources
        
        Args: user_matches (list[dict]) list of dictionaries with relevant information for that
        make, model, year, and part
        
        Returns: None. Takes Same information turns into self.df (pandas DatFrame)"""

        self.df = pd.DataFrame(user_matches)
    
    def user_menu(self) -> None:
        """Function to manipulate the pandas data frame and let the user view their matches
        
        Args: None
        
        Returns: None"""

        if isinstance(self.df, type(None)):
            sys.exit("There are no results for your query. Try a new query.")
        

    