import argparse
import os
import sys

import pandas as pd

import local_data_pull as ld_pull

class DataFrameQueryTerminal:
    """Simple terminal interface for querying pandas DataFrames."""
    
    def __init__(self, dataframe):
        self.df: pd.DataFrame = dataframe
        self.main_menu: list = ["Sort", "Filter", "Price", "Save", "Quit", "Ascending", "Descending", "true", "false"]
        self.boolean_operators: dict = {'LT': '<', 'LTEQ': '<=', 'GT': '>', 'GTEQ': '>=', 'EQ': '=='}
        self.logical_operators: dict = {'AND': '&', 'OR': '|', 'NOT': '~'}
        
    def help_info(self) -> None:
        """Prints out helpful information for the user"""
        help_text = f"""Filter and Sort Queries available are related to these columns {list(self.df.columns)}
Options: 
-Sort == Sort results based upon column of choice
-Filter == Filter results based upon colunn(s) of choice (boolean search allowed)
-Save == Save results as a Comma Seperated Values (.csv) file
-Quit == Quit the program"""
        print(help_text)      
    
    def _filter(self, user_input_str: str) -> pd.DataFrame:
        """Takes parsed args if -filter is present and returns a filtered dataframe.
        
        args: arg_parser (argparse.ArgumentParser) the arguments from self.user_input
        
        returns: filtered dataframe"""
        better_list = [word.replace("-", "") for word in user_input_str.split(" ")[1:]]
        if "Sort" in better_list:
            index_point = better_list.index("Sort")
            del better_list[index_point: index_point + 4]
        query_string = ""

        print(better_list)
        for word in better_list:
            if word in self.boolean_operators:
                query_string += f" {self.boolean_operators.get(word)} "
                continue
            
            if word in self.logical_operators:
                query_string += f" {self.logical_operators.get(word)} "
                continue

            query_string += f" {word} " 

        return self.df.query(query_string)
        

        
    def build_parser(self) -> str:
        """Gathers input from the user and parses it out. Returns the parsed argument as a 
        dictionary
        
        Args: None
        
        Returns: filtered_dict (dict) dictionary of the arguments and what the selected 
        options were if the options are not None."""


        self.help_info()
        user_decision = input("")

        parser = argparse.ArgumentParser()

        parser.add_argument("-Sort", required = False, choices = list(self.df.columns))
        parser.add_argument("-Filter", required = False, choices = list(self.df.columns))
        parser.add_argument("-Save", required = False)
        parser.add_argument("-Quit", required = False)
        parser.add_argument("-Ascending", required = False)
        parser.add_argument("-Descending", required = False)
    
        # Add in boolean options
        for bool_operator in self.boolean_operators:
            parser.add_argument(f"-{bool_operator}", required = False)
        
        for logic_operator in self.logical_operators:
            parser.add_argument(f"-{logic_operator}", required = False)

        args = parser.parse_args(user_decision.split(" "))

        
        if hasattr(args, "Sort") and (not hasattr(args, "Ascending") or not hasattr(args, "Descending")):
            sys.exit("Sort requires Ascending or Descending arguments")

        

        return user_decision
        
    def make_selection(self) -> None:
        """Takes the return from build_parser and selects the correct function to run.
        
        Args: None
        
        Returns: None, decides the function to run"""


        user_input = self.build_parser()

        filter_test = user_input.find("Filter")

        if filter_test != -1:
            new_df = self._filter(user_input)
        
        print(new_df)

if __name__ == "__main__":
    parent_dir = ld_pull.get_top_level_directories().get("parent_directory")
    test_csv_path = os.path.join(parent_dir, "test.csv")
    df = pd.read_csv(test_csv_path)

    test_obj = DataFrameQueryTerminal(df)
    test_obj.make_selection()
    
    

