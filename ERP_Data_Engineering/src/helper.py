import datetime
import os
import shutil
from pathlib import Path

def day_of_week_fun() -> int:
    day_of_week_input = input("What day of the week do you want to run? Monday or Thursday?").lower()
    if day_of_week_input[0] == "m":
        day_of_week = 0
    else:
        day_of_week = 3
    
    return day_of_week

def manual_override():
    override_option = input("Do you want to manually override the program to run data loads? Y/N?").lower()
    
    if override_option[0] == "y":
        return day_of_week_fun()
   
    return None
    

def day_of_week_check():
    """This function is designed to check the day of the week. If the day is Monday different files are 
    are downloaded as opposed to Thursday. Also data loads are only done Mondays or Thursdays so if it is ran
    on a day that is not Monday or Thursday the program will terminate. Later there will be a function to have 
    the user pick which day of the week they need to run in case of a failure on Monday or Thursday"""
    today_str = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    today_year = int(today_str[:4])
    today_month = int(today_str[5:7])
    today_day = int(today_str[-2:])
    day_of_week = int(datetime.date(today_year, today_month, today_day).weekday())
    print('Day of week checked!')
    
    if day_of_week not in (0,3):
        return manual_override(), today_str
    
    return day_of_week, today_str

def get_current_dir() -> str:
    """Returns current directory file is running in.
    
    Args: None
    
    Returns: current directory file is being run in."""
    return os.path.dirname(os.path.abspath(__file__))


def get_user_creds() -> str:
    current_dir = get_current_dir()
    keys_path = os.path.abspath(os.path.join(current_dir, "..", "keys"))
    obi_user_path = os.path.abspath(os.path.join(keys_path, "obi_user.txt"))
    obi_pw_path = os.path.abspath(os.path.join(keys_path, "obi_pw.txt"))

    sf_user_path = os.path.abspath(os.path.join(keys_path, "sf_user.txt"))
    sf_pw_path = os.path.abspath(os.path.join(keys_path, "sf_pw.txt"))
    sf_key_path = os.path.abspath(os.path.join(keys_path, "sf_key.txt"))

    credentials_dict = {}

    with open(obi_user_path) as obi_user_data:
        obi_username = obi_user_data.read()
        credentials_dict["obi_username"] = obi_username
    
    with open(obi_pw_path) as obi_pw_data:
        obi_password = obi_pw_data.read()
        credentials_dict["obi_password"] = obi_password
    
    with open(sf_user_path) as sf_user_data:
        sf_user = sf_user_data.read()
        credentials_dict["sf_user"] = sf_user
    
    with open(sf_pw_path) as sf_pw_data:
        sf_password = sf_pw_data.read()
        credentials_dict["sf_password"] = sf_password
    
      
    with open(sf_key_path) as sf_key_data:
        sf_key = sf_key_data.read()
        credentials_dict["sf_password"] = sf_key
    
    return credentials_dict


def move_files(file: str, destination: Path) -> None:
    downloads_dir: str = rf'C:\Users\wxm3287\Downloads\\'
    file_in_downlads: str = downloads_dir + file
    destination_file = destination + file
    shutil.move(file_in_downlads, destination_file)

def attachment_rate_rename(current_date) -> dict:
    attachment_rate_dict = {0:'Onward 6P by date.csv', 1: 'Onward Accessories - 2023 Attachment Rate.xlsx'}

    filename = r'C:\Users\wxm3287\Downloads\Onward Accessories - 2023 Attachment Rate.xlsx'

    basename, extension = os.path.splitext(filename)

    new_filename = f'{basename} {current_date}{extension}'
    os.rename(filename, new_filename)

    slice_begin = new_filename.rfind('\\')
    onward_accessories = new_filename[slice_begin+1:]
    attachment_rate_dict[1] = onward_accessories

    return attachment_rate_dict

def move_and_rename_files(weekday):
    """This function takes the current files and moves them to their desginated location in the 'K' drive
    One file needs to be renamed every Monday and that file alone will be renamed with the current date in 
    YYYY-MM-DD format."""
    day_of_week, current_date = weekday

    reference_data_dict = {0:'PLAN ETL - Objectives Data.csv', 1:'PLAN ETL - Plan Data.csv', 2: 'Warr Reg Flag CY.csv', 3: 'Warranty Accepted Amount CY for SFDC updates.csv', 4:'Warranty Registrations for SFDC updates.csv', 5: 'Order - Details for WR CY.csv'}
    
    for position, reference_data_file in reference_data_dict.items():
        destination_path = rf'\\AGS-US-303\Specdata\Analytics_Reports\Reference Data\\'
        move_files(destination=destination_path, file=reference_data_file)
    
    if day_of_week == 0:
        attachment_rate_dict: dict = attachment_rate_rename(current_date=current_date)

        for position, attachment_rate_file in attachment_rate_dict.items():
            destination_path = rf'K:\Analytics_Reports\Reference Data\AttachmentRate\\'
            move_files(file=attachment_rate_file, destination=destination_path)