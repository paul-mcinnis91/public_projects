import datetime
import os
import sys
import time

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.OBI_Downloads import DownloadFilesfromOBI
from src.helper import day_of_week_check, move_and_rename_files

def download_files_from_OBI(weekday):
    get_files = DownloadFilesfromOBI(weekday)
    get_files.download_files()
    get_files.download_missed_files()

def main():
    """This function acts as the Main() function would in a C program. Or at least a rudimentary 
    version of the Main() function. This combines all previous functions and runs the program
    Later there will be an associated text document with this program that will keep track of unsuccessful
    vs successful runs"""
    start_time = time.time()
    date_information = day_of_week_check()
    download_files_from_OBI(date_information)
    print(datetime.datetime.now())
    move_and_rename_files(date_information)
    run_time = (time.time()-start_time)/60
    print(f'Program completed in {run_time} minutes!')
    end_time = datetime.datetime.now()
    with open("weekly_data_loads_performance.csv", "a+") as WDLP:
        WDLP.write(f"{datetime.datetime.today().strftime('%Y-%m-%d')},{start_time},{run_time},{end_time}")
        WDLP.write("\n")
    
    sys.exit()



if __name__ == "__main__":
    main()