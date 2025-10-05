import argparse
import sys
import os

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.hollander import Hollander
from src.query_df import DataFrameQueryTerminal



def main() -> None:
    """Main function to run Car Parts Web Crawler Module"""

    parser = argparse.ArgumentParser(description="Car info parser")

    parser.add_argument("-y", "--year", type = int, required = True, help = "Car year")
    parser.add_argument("-make", required = True, help = "Car make")
    parser.add_argument("-model", required = True, help = "Car model")
    parser.add_argument("-p", "--parts", required = True, help = "Car Part")

    args = parser.parse_args()

    hollander_obj = Hollander(year = args.year, make= args.make, model = args.model)
    part_list = hollander_obj.get_parts(part = args.parts)
    
    hollander_obj.create_user_matches(user_matches = part_list)

    df_terminal_menu = DataFrameQueryTerminal(hollander_obj.df)

    df_terminal_menu.run()
    
    
   




if __name__ == "__main__":

    main()