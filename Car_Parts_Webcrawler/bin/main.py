import sys
import os

import pandas as pd

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)


from src.local_terminal import Query_Df
from src.web_terminal import Query_Webpages
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push



def main() -> None:
    """Main function to run Car Parts Web Crawler Module"""

    local_df = ld_pull.build_records_keeping_df()
    print(local_df)
    local_df_query = Query_Df(local_df)
    local_df_query.run()

    sys.exit("Goodbye")
    web_query_obj = Query_Webpages()
    part_list = web_query_obj.run_webpage()
    
    web_query_obj.create_user_matches(user_matches = part_list)

    csv_path = ld_push.csv_file_name(car_year = web_query_obj.year, 
                                    car_make = web_query_obj .make,
                                    car_model = web_query_obj.model,
                                    car_part = web_query_obj.part)
    
    ld_push.save_csv_records(df = web_query_obj.df, csv_file_path = csv_path)

    query_selections = ld_pull.package_records_keeping()
    
    df_path = web_query_obj.create_user_matches(query_selections)

    df = pd.read_csv(df_path, index_col = 0)


    df_query = Query_Df(df)
    df_query.run()


if __name__ == "__main__":

    main()