import argparse
import sys
import os

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src import local_data_pull as ld_pull
from src.local_terminal import Query_Df
from src.web_terminal import Hollander


def help_info() -> None:
        """Function to print this terminal's help information"""
        help_text = f"""
Options: 
-View == View available tables and pick one or exit the program
-Create == Create new table or exit the program
-Quit == Quit the program
-Help == View this information again
"""
        print(help_text)     

def main() -> None:
  
    parser  = argparse.ArgumentParser()
    parser.add_argument("-View", required = False, action = "store_true")
    parser.add_argument("-Create", required = False, action = "store_true")
    parser.add_argument("-Quit", required = False, action = "store_true")
    parser.add_argument("-Help", required= False, action = "store_true")

    args = parser.parse_args()

    if args.Help:
        help_info()
        
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
        hollander_obj.get_parts()
        

if __name__ == "__main__":
    main()