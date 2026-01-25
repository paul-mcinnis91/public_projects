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

    # Creating file path where document will be saved.
    today_date = date.today()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(current_dir, "..", "source_documents", f"{today_date}_111_driving_distances.csv"))

    if len(sys.argv) < 2:
        # Creating option to run both with and without email input
        sys.exit("No arguments received")

    data_validation_obj = Ingest_Data(sys.argv[1])

        
    
    unscrubbed_csv = sys.argv[1]
    if "HORs.csv" not in unscrubbed_csv:
        sys.exit(f"Looking for file called HORs.csv got {unscrubbed_csv}")
    scrubbed_csv = data_validation_obj.validate_file(hor_csv_path=unscrubbed_csv)
    drving_distance_obj = Driving_Distance(scrubbed_csv)
    df: pd.DataFrame = drving_distance_obj.get_time_and_distance()

    # Saving document
    df.to_csv(csv_path, index=False)

    sys.exit()