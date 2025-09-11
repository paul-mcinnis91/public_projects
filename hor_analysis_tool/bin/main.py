#!/usr/bin/env python3
import os
import sys
import pandas as pd
from datetime import date

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.driving_distance import Driving_Distance
from src.ingest_data import Ingest_Data


if __name__ == "__main__":

    data_validation_obj = Ingest_Data()

    # Creating file path where document will be saved.
    today_date = date.today()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(current_dir, "..", "source_documents", f"{today_date}_111_driving_distances.csv"))

    if len(sys.argv) == 1:
        # Creating option to run both with and without email input
        scrubbed_hor_csv = data_validation_obj.mov_file()
        drving_distance_obj = Driving_Distance(scrubbed_hor_csv)
        df: pd.DataFrame = drving_distance_obj.get_time_and_distance()
        
    if len(sys.argv) == 2:
        # Adding in a way to run with command line arguments to bypass email requirements
        unscrubbed_csv = sys.argv[1]
        if "HORs.csv" not in unscrubbed_csv:
            raise ValueError(f"Looking for file called HORs.csv got {unscrubbed_csv}")
        scrubbed_csv = data_validation_obj.mov_file(hor_csv_path=unscrubbed_csv)
        drving_distance_obj = Driving_Distance(scrubbed_csv)
        df: pd.DataFrame = drving_distance_obj.get_time_and_distance()

    # Saving document
    df.to_csv(csv_path, index=False)

    exit()