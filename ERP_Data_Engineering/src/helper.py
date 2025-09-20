import datetime
import os

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
    user_path = os.path.abspath(os.path.join(keys_path, "user.txt"))
    pw_path = os.path.abspath(os.path.join(keys_path, "pw.txt"))

    credentials_dict = {}

    with open(user_path) as user_data:
        username = user_data.read()
        credentials_dict["username"] = username
    
    with open(pw_path) as pw_data:
        password = pw_data.read()
        credentials_dict["password"] = password
    
    return credentials_dict