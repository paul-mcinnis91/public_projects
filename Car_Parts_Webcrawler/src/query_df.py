import argparse
import sys
import pandas as pd

class DataFrameQueryTerminal:
    """Simple terminal interface for querying pandas DataFrames."""
    
    def __init__(self, dataframe):
        self.df: pd.DataFrame = dataframe
        
    def help_info(self) -> None:
        """Prints out helpful information for the user"""
        help_text = f"""Queries available are related to these columns {list(self.df.columns)}
Options: 
-Sort / --s == Sort results based upon column of choice
-Filter / --f == Filter results based upon colunn(s) of choice (boolean search allowed)
-Save == Save results as a Comma Seperated Values (.csv) file
-Quit / --q == Quit the program"""
        print(help_text)

    def user_input(self) -> None:
        """Gathers input from the user and parse it out. Based upon the parsed information, 
        selects the appropriate function to run"""


        parser.add_argument("-Sort", "--s", required = False)
        parser.add_argument("-Fiter", "--f", required = False)
        parser.add_argument("-Save", required = False)
        parser.add_argument("-Quit", "--q", required = False)
        parser.add_argument("&&", "AND", required = False, type = float)
        parser.add_argument("||", "OR", required = False, type = float)
        parser.add_argument("<>", "NOT", required = False, type = float)
        parser.add_argument("<", required = False, type = float)
        parser.add_argument("<=", required = False, type = float)
        parser.add_argument(">", required = False, type = float)
        parser.add_argument(">=", required = False, type = float)
        parser.add_argument("=", required = False, type = float)


        self.help_info()
        user_decision = input("")

        parser = argparse.ArgumentParser(user_decision.split())

        parser.parse_args()

        if not vars(parser):
            print("No Arguments Presented. Pick an argument")
        


