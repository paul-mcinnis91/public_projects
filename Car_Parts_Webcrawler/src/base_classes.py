import argparse
import sys

import pandas as pd


class User_Interface:
    def __init__(self):
        self.df = None

    def _get_int(self, input_str: str) -> int:
        
        if input_str[0] == 'q':
            sys.exit("No choice selected")

        while True:
            try:
                user_input = input(input_str + " ")
                int_input = int(user_input)
                return int_input
            except ValueError:
                print("Invalid input. Try Again.")

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
        user_part_choice = self._get_int("Select your choice by the number next to it. If your choice is not present, type quit ").lower()

        int_key = user_part_choice
        str_key = display_dict[int_key]
        return matches_dict[str_key]
        
        
    
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

        if self.df is None:
            sys.exit("There are no results for your query. Try a new query.")


class Query_Webpages:

    def __init__(self):
        self.part: str = None
        self.get_counter: int = 0

    def help_info(self):
        """Prints out helpful information for the user"""
        help_text = f"""Filter and Sort Queries available are related to these columns:
Options: 
-Query == Create a new web query that will add to the tables currently available
          When Query is ran it requires the args: -year <car year>
                                                  -make <car make>
                                                  -model <car model>
                                                  -part <car part>
-Quit == Quit the program
-Help == Prints this text so you have a reference"""
        print(help_text)
    
    def _build_web_menu(self) -> argparse.Namespace:
        """Builds the actual argumentparser object with the car information to pass on"""

        parser = argparse.ArgumentParser(description="Car info parser")
       
        user_decision = input("Enter your command here: ").strip()

        parser = argparse.ArgumentParser()
        parser.add_argument("-Query", action = "store_true", help = "Run a web query")
        parser.add_argument("-Quit", action = "store_true", help = "Quit program")
        parser.add_argument("-Help", action = "store_true", help = "View help text")
        parser.add_argument("-make", type=str, help = "Car make")
        parser.add_argument("-model", type=str, help = "Car model")
        parser.add_argument("-year", type=str, help = "Year")
        parser.add_argument("-part", type=str, help = "Part")

        args = parser.parse_args(user_decision.split(" "))

        return args
    
    def _check_query_args(self, args: argparse.Namespace) -> bool:
        query_req_args = ["make", "model", "year", "part"]
        missing = [name for name in query_req_args if getattr(args, name) is None]
        if missing:
            sys.exit("Query arg required -year -make -model and -part flags")

    def _parse_user_input(self) -> list:
        """Determines what function will be ran based upon the arguments passed into it
        
        Args: None uses self.build_web_menu to determine what the user picked
        
        Returns: None, picks the function"""

        args = self._build_web_menu()

        if args.Query:
            self._check_query_args(args)
            self.year = args.year
            self.make = args.make
            self.model = args.model
            self.part = args.part

        if args.Quit:
            sys.exit("Goodbye.")
        
        if args.Help:
            self.help_info()

    
    def run_webpage(self) -> None:
        """Gets user input to actually get the parts information"""

        self.help_info()

        while True:
            try:
                self._parse_user_input()
            except KeyboardInterrupt:
                sys.exit("Keyboard interrupt detected. Exiting.")

