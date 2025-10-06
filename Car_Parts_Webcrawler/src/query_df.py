import argparse
import os

import pandas as pd

import local_data_pull as ld_pull

class DataFrameQueryTerminal:
    """Simple terminal interface for querying pandas DataFrames."""
    
    def __init__(self, dataframe):
        self.df: pd.DataFrame = dataframe
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

    def _filter(self, args: list) -> pd.DataFrame:
        """Takes parsed args if -filter is present and returns a filtered dataframe.
        
        args: arg_parser (argparse.ArgumentParser) the arguments from self.user_input
        
        returns: fitlered dataframe"""
        print(args)
        for idx, word in enumerate(args):
            if word in self.boolean_operators:
                args[idx] = self.boolean_operators.get(word)
            
            if word in self.logical_operators:
                args[idx] = self.logical_operators.get(word)
        
        new_query_string = " ".join(args)
        print(new_query_string)

        
        

    def user_input(self) -> None:
        """Gathers input from the user and parse it out. Based upon the parsed information, 
        selects the appropriate function to run"""


        self.help_info()
        user_decision = input("")

        parser = argparse.ArgumentParser()

        parser.add_argument("-Sort", required = False, choices = self.df.columns)
        parser.add_argument("-Filter", required = False, choices = self.df.columns)
        parser.add_argument("-Save", required = False)
        parser.add_argument("-Quit", required = False)

    
        # Add in boolean options
        for bool_operator in self.boolean_operators:
            parser.add_argument(f"-{bool_operator}", required = False)
        
        for logic_operator in self.logical_operators:
            parser.add_argument(f"-{logic_operator}", required = False)

        args = parser.parse_args(user_decision.split(" "))


        if not vars(parser):
            print("No Arguments Presented. Pick an argument")

        if any(getattr(args, op) is not None for op in self.boolean_operators):
            if not (args.Filter or args.Sort):
                parser.error("Operators require -Filter or -Sort")
        
        args_list = list(vars(args).values())

        if hasattr(args, "Filter"):
            self._filter(args_list)
        

if __name__ == "__main__":
    parent_dir = ld_pull.get_top_level_directories().get("parent_directory")
    test_csv_path = os.path.join(parent_dir, "test.csv")
    df = pd.read_csv(test_csv_path)

    test_obj = DataFrameQueryTerminal(df)
    test_obj.user_input()
    
    

