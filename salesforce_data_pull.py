import datetime
import pandas as pd
from salesforce_reporting import Connection
import csv
import openpyxl
from numpy import array
import sys



def salesforce_UVO_pull():
    """This portion of the program uses API data to pull the UVO Audit All Years Report from Salesforce and return it as a list
    It is pulled before the data is transferred and after the data is transferred to ensure there was a change in the data"""
    # Salesforce API credentials
    username = 'paul.mcinnis@clubcar.com'
    password = 'Clubcar$3005'
    security_token = 'kneihXRgsDQ3hWzo1owJl4JeO'
    
    """"We keep the following lines just in case we need it later"""
    # SFDC Key info
    # Client ID
    # SFDC_consumer_key = '3MVG9kBt168mda__uvsaWSEjwpyL6OdK3gEzrvI0rUhKDjMxQbCW9bidJY3mVhR2yTDFu8Ihgg8ELYFEUWltl'
    # Client Secret
    # SFDC_consumer_secret = 'D7AFC04FDE47BD6B2F016FD9B6CD55C436024D3C147C09579088EF9E69DD25A8'
    """********************************************************************************************************"""
    report_id = '00O4x000007MOXJEA4'

    # The UVO data is broken down by year. Each row is a year, row 10 is year 23. So to make sure we get the right data every year 
    # We have created an algorithm which takes the current two digit year and subtracts 13 from it to ensure we are on the right row

    full_date = datetime.datetime.today()
    four_digit_year = str(full_date.year)
    year = int(four_digit_year[-2:])
    row_pointer = year - 13


    
    login_for_full_report = Connection(username= username,
                                        password= password,
                                        security_token=security_token)
    full_report: dict = login_for_full_report.get_report(report_id)
    data_frame = pd.DataFrame(full_report)
    """The following portion is to write a pandas data frame to a csv file for comparison We keep the line below in case we have issues 
    with data and need see what the actual file looks like and make adjustments"""
    objective_data = data_frame['factMap'][f'{row_pointer}!0']['aggregates']
    plan_data = data_frame['factMap'][f'{row_pointer}!0']['aggregates']
    plan_plus_objective = data_frame['factMap'][f'{row_pointer}!T']['aggregates']

    current_year_data = [data['value'] for data in objective_data + plan_data + plan_plus_objective]
    
    return current_year_data

current_data = salesforce_UVO_pull()
current_time = datetime.datetime.now().replace(second=0, microsecond=0)
print(current_time)
current_data.insert(0, str(current_time))
print(current_data)

SUD_excel = openpyxl.load_workbook(r"K:\Augusta Sales Support\Club Car CX Systems & Data Management\Data Analyst\Python Files\Weekly Data Loads\Salesforce Data\Salesforce_UVO_data.xlsx")
SUD_excel_Sheet1 = SUD_excel.get_sheet_by_name("Sheet1")
SUD_excel_Sheet1.append(current_data)
SUD_excel.save(r"K:\Augusta Sales Support\Club Car CX Systems & Data Management\Data Analyst\Python Files\Weekly Data Loads\Salesforce Data\Salesforce_UVO_data.xlsx")



with open(r"K:\Augusta Sales Support\Club Car CX Systems & Data Management\Data Analyst\Python Files\Weekly Data Loads\Salesforce Data\Salesforce_UVO_data.csv", "a", newline='') as SUD_csv:
    writer = csv.writer(SUD_csv)
    writer.writerow(current_data)
sys.exit()

