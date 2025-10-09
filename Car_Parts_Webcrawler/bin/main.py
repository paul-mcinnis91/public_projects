import argparse
import sys
import os

import pandas as pd

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.hollander import Hollander
from src.query_df import DataFrameQueryTerminal
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push



def main() -> None:
    """Main function to run Car Parts Web Crawler Module"""

    parser = argparse.ArgumentParser(description="Car info parser")

    parser.add_argument("-y", "--year", type = int, required = True, help = "Car year")
    parser.add_argument("-make", required = True, help = "Car make")
    parser.add_argument("-model", required = True, help = "Car model")
    parser.add_argument("-p", "--parts", required = True, help = "Car Part")

    args = parser.parse_args()

    hollander_obj = Hollander(year = args.year, make = args.make, model = args.model)
    part_list = hollander_obj.get_parts(part = args.parts)
    
    hollander_obj.create_user_matches(user_matches = part_list)

    csv_path = ld_push.csv_file_name(car_year = args.year, 
                                    car_make = args.make,
                                    car_model = args.model,
                                    car_part = args.parts)
    ld_push.save_csv_records(df = hollander_obj.df, csv_file_path = csv_path)

    df = pd.read_csv(csv_path, index_col = 0)

    df_query = DataFrameQueryTerminal(df)
    df_query.run()
    
    
   




if __name__ == "__main__":

    main()