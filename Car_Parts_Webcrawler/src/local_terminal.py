import argparse
import os
from pathlib import Path
import sys
import time

import pandas as pd

from src import local_data_pull as ld_pull
from src.base_classes import User_Interface
from src.web_terminal import Hollander

class Query_Df(User_Interface):
    """Simple terminal interface for querying pandas DataFrames."""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df: pd.DataFrame = self._convert_numeric_columns(dataframe)
        self.main_menu: list = ["Sort", "Filter", "Price", "Save", "Quit", "Ascending", "Descending"]
        self.boolean_operators: dict = {'LT': '<', 'LTEQ': '<=', 'GT': '>', 'GTEQ': '>=', 'EQ': '=='}
        self.logical_operators: dict = {'AND': '&', 'OR': '|', 'NOT': '~'}
        self.manipulated_df = None
        
    def help_info(self) -> None:
        """Prints out helpful information for the user"""
        help_text = f"""Filter and Sort Queries available are related to these columns:
{list(self.df.columns)}
Options: 
-Sort == Sort results based upon column of choice. 
         Defaults to Ascending unless Descending is supplied as an option
-Filter == Filter results based upon column(s) of choice (boolean search allowed)
-Quit == Quit the program
-View == View current results of query. Built into -Filter and -Sort. 
         Can view one or more column(s) by using -View <col_name1> <col_name2>. 
         If no columns provided willl print full dataframe
-Help == Prints this text so you have a reference
-Open == If you are dealing with the local data files this option will be available
         Requires file path -Open <FILE_PATH> 
-Save == Save results as a Comma Seperated Values (.csv) file. 
         Only available if -Open is not"""
        

        print(help_text)

    def _open(self, file_path: Path) -> pd.DataFrame:
        """Takes a file path to a csv and turns it into a pandas DataFrame
        
        Args: file_path (Path)
        
        Returns: pd.DataFrame"""

        df = pd.read_csv(file_path, index_col = 0)
        return df

    def _view(self, view_args: list) -> None:
        """Checks if self.manipulated_df is None. If it is, prints self.df Otherwise prints
        self.manipulated_df. If col_name is supplied will print just that column's information"""

        if len(view_args) == 0:
            view_args = self.df.columns

        if self.manipulated_df is None:
            print(self.df[view_args])
            return None
        
        print(self.manipulated_df[view_args])
        return None
    
    def _scrub_args(self, user_input_str: str) -> list:
        """Takes user_input_str and turns it into a list without dashes
        
        Args: user_input_str (str) what the user input into the string
        
        Returns: better_list (list) list format of user_input_str stripped of dashes"""

        return [word.replace("-", "") for word in user_input_str.split(" ")[1:]]

    def _test_sort_order(self, sort_args: list) -> bool:
        """Takes the arguments from sort_args and determines if the second value is ascending,
        descending, or nonexistent. If ascending or nonexistent, returns true. Otherwise returns
        False.
        
        Args: sort_args (list) list of the args from args.Sort
        
        Returns: bool True for ascending or nonexistant."""

        string_args = " ".join(sort_args).lower()

        if "descend" in string_args:
            return False
        
        return True

    def _sort(self, sort_args: list) -> pd.DataFrame:
        """Takes user input str and returns a sorted Dataframe
        
        args: user_input_str (str) the arguments from self.user_input
        
        returns: sorted dataframe"""
        
        column_name = sort_args[0]
        order = self._test_sort_order(sort_args)

        if self.manipulated_df is None:
            sorted_df = self.df.sort_values(by = column_name, ascending = order)
            self.manipulated_df = sorted_df
            self._view(sorted_df.columns)
            return sorted_df
        
        sorted_df = self.manipulated_df.sort_values(by = column_name, ascending = order)
        self.manipulated_df = sorted_df
        
        self._view(sorted_df.columns)
        return sorted_df
    
    def _filter(self, user_input_str: str) -> pd.DataFrame:
        """Takes parsed args if -filter is present and returns a filtered dataframe.
        
        args: user_input_str (str) the arguments from self.user_input
        
        returns: filtered dataframe"""
        better_list = self._scrub_args(user_input_str)

        query_string = ""

        for word in better_list:
            if word in self.boolean_operators:
                query_string += f" {self.boolean_operators.get(word)} "
                continue
            
            if word in self.logical_operators:
                query_string += f" {self.logical_operators.get(word)} "
                continue

            query_string += f" {word} " 
        
        filtered_df = self.df.query(query_string).reset_index(drop=True)

        self.manipulated_df = filtered_df

        self._view(self.manipulated_df.columns)
        return filtered_df
    
    def _save(self, new_df: pd.DataFrame) -> None:
        """Function to save the file name based upon user input
        
        Args: new_df (pd.DataFrame) the new_df supplied from the user_input function
        
        Returns: None, saves the file to the records_keeping directory"""


        records_dir = ld_pull.get_top_level_directories().get("records_keeping")
        user_file_name = input("Type the name of your file. ")
        removed_file_ext = os.path.splitext(user_file_name)[0] 
        csv_path = os.path.join(records_dir, removed_file_ext + ".csv")
        new_df.to_csv(csv_path, index = False)
        
    def _numeric_conversion(self, series: pd.Series) -> pd.Series:
        """Checks if a column has numeric valuies. If does returns the column with 
        all text values converted to 0s and regular text turned to floats.
        
        Args: series (pd.Series) the column to be tested
        
        Returns: series (pd.Series) the column in it's original form or converted"""
        numeric_count = pd.to_numeric(series, errors='coerce').notna().sum()
        if numeric_count > 0:
            new_series = pd.to_numeric(series, errors='coerce').fillna(0)
            return new_series
        
        return series 

    def _convert_numeric_columns(self, df: pd.DataFrame):
        """Takes pandas dataframe, finds all columns with numeric columns and converts them from 
        string to numeric columns.
        
        Args: df (pandas.DataFrame) the dataframe to have it's columns converted
        
        Returns: converted dataframe"""
        for col in df.columns:  
            # Create a test series - strip whitespace and remove common formatting
            test_series = df[col].astype(str).str.strip()
            
            # Remove common price/number formatting (commas, dollar signs)
            test_series = test_series.str.replace('$', '', regex=False)
            test_series = test_series.str.replace(',', '', regex=False)

            numeric_count = pd.to_numeric(test_series, errors='coerce').notna().sum()
            if numeric_count > 0:
                new_series = pd.to_numeric(test_series, errors='coerce').fillna(0)
            
                df[col] = new_series

            df.reset_index(drop = True)

        return df
        
    def _build_parser(self) -> tuple:
        """Gathers input from the user and parses it out. Returns the parsed argument as a 
        dictionary
        
        Args: None
        
        Returns: filtered_dict (dict) dictionary of the arguments and what the selected 
        options were if the options are not None."""

        user_decision = input("Enter your command here: ").strip()

        parser = argparse.ArgumentParser()

        df_columns_list = list(self.df.columns)
        

        parser.add_argument("-Sort", required = False, nargs="+", metavar=('COLUMN', 'ORDER'))
        parser.add_argument("-Filter", required = False, choices = df_columns_list)
        parser.add_argument("-Quit", required = False, nargs ="?", default = "None", const = "None")
        parser.add_argument("-View", required = False, nargs = "*", default = df_columns_list)
        parser.add_argument("-Help", required=False, nargs = "?")

        if "File Path" in df_columns_list:
            parser.add_argument("-Open", required = False, nargs="+", metavar=('FILE PATH'))
    
        else:
            parser.add_argument("-Save", required = False, nargs ="?", default = "None", const = "None")

        # Add in boolean options
        for bool_operator in self.boolean_operators:
            parser.add_argument(f"-{bool_operator}", required = False)
        
        for logic_operator in self.logical_operators:
            parser.add_argument(f"-{logic_operator}", required = False)

        args = parser.parse_args(user_decision.split(" "))


        return (user_decision, args)
        
    def make_selection(self) -> None:
        """Takes the return from build_parser and selects the correct function to run.
        
        Args: None
        
        Returns: None, decides the function to run and then updates self.manipulated_df"""


        user_input, args = self._build_parser()


        filter_test = user_input.find("Filter")
        save_test = user_input.find("Save")
        quit_test = user_input.find("Quit")
        view_test = user_input.find("View")
        help_test = user_input.find("Help")       

        new_df = self.df
        if self.manipulated_df is not None:
            new_df = self.manipulated_df

        if view_test != -1:
            self._view(args.View)
            
        if filter_test != -1:
            new_df = self._filter(user_input)
        
        if args.Sort:
            new_df = self._sort(args.Sort)

        if save_test != -1:
            self._save(new_df)
        
        if quit_test != -1:
            sys.exit("Have a nice day, goodbye.")
        
        if help_test != -1:
            self.help_info()
        
        if args.Open:
            print(new_df)
            user_index = self._get_int("Select the number next to the file path you want")
            file_path = new_df["File Path"][user_index]
            pass_up_df = self._open(file_path)
            return pass_up_df

        self.manipulated_df = new_df
        
    def run(self):
        """Runs infinite loop until user puts in quit command
        
        Args: None
        
        Returns: None"""
        self.help_info()

        try:
            while True:
                pass_up_df: pd.DataFrame = self.make_selection()
                if pass_up_df is not None:
                    return pass_up_df

        
        except KeyboardInterrupt:
            sys.exit("Keyboard interrupt detected. Shutting down")
        
        except SystemExit:
            print("Unknown arguments detected. Pick an argument from below.")
            time.sleep(3)
            self.help_info()


class Main_Menu(User_Interface):
    def __init__(self):
        super().__init__()
    
    def help_info(self) -> None:
        """Function to print this terminal's help information"""
        help_text = f"""
Options: 
-View == View available tables and pick one or exit the program
-Create == Create new table or exit the program
-Quit == Quit the program
-Help == View this information again
"""
        print(help_text)
    
    def _build_arg_parser(self) -> None:
        """Function to build main menus argument parser.
        
        Args: None
        
        Returns: None"""

        parser = argparse.ArgumentParser()
        parser.add_argument("-View", required = False, nargs ="?")
        parser.add_argument("-Create", required = False, nargs ="?")
        parser.add_argument("-Quit", required = False, nargs ="?")
        parser.add_argument("-Help", required=False, nargs = "?")

        return parser.parse_args()
    
    def run(self) -> None:
        """Function to run the main menu"""

        args = self._build_arg_parser()

        if args.Help:
            self.help_info()
        
        if args.Quit:
            sys.exit("Goodbye.")
        
        if args.View:
            local_df = ld_pull.build_records_keeping_df()
            table_viewer = Query_Df(local_df)
            archived_df = table_viewer.run()
            if archived_df is not None:
                archive_viewer = Query_Df(archived_df)
                archive_viewer.run()

        if args.Create:
            hollander_obj = Hollander()
            hollander_obj.run_webpage()


