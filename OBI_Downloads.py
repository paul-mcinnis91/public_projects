import time
import datetime
import shutil
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException
from collections import OrderedDict
import pandas as pd
from numpy import array
import sys

"""The purpose of this program is to download multiple files from Oracle Business Intelligence and place
the files into the appropriate folder in the 'K' Drive. This is done by webcrawling using Selenium 
for now and will later be changed to ODBC access or API access."""

def manual_override():
    override_option = input("Do you want to manually override the program to run data loads? Y/N?").lower()
    if override_option[0] == "y":
        day_of_week_input = input("What day of the week do you want to run? Monday or Thursday?").lower()
        if day_of_week_input[0] == "m":
            day_of_week = 0
        elif day_of_week_input[0] == "t":
            day_of_week = 3
    else:
        return None
    
    return day_of_week

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

class DownloadFilesfromOBI:
    def __init__(self, weekday) -> None:
        self.weekday = weekday
    

    def OBI_Login(self):
        """This function starts Selenium / Webcrawling and logins into Oracle Business Inelligence. 
        It uses the current users login info to achieve this. This needs to be changed in the future to a 
        generic user such as the system Admin"""
    
        user_ID = 'WXM3287'.upper()
        password = 'PropelOnward$3005'
        login_URL = r'http://ccinsight.internal.clubcar.com:9502/bi-security-login/login.jsp?msi=false&redirect=L2FuYWx5dGljcy9zYXcuZGxsP2JpZWVob21lJnN0YXJ0UGFnZT0xJmhhc2g9ajdETVBqQkk2N2l4NHBQbU1FTURnbmNhTGZmai00NmRDOVRKMUlmdzBfTkdWdHpzLWs3YjJQSkJrZDJ6QUc1Yg=='

        quiet = Options()
        quiet.add_argument('-headless')

        driver = webdriver.Firefox(options=quiet, service=FirefoxService(r'wrongpath'))
        driver.get(login_URL)
        
        user_ID_field_xpath ='//*[@id="idUser"]'
        
        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, user_ID_field_xpath))).click()
        driver.find_element(By.XPATH, user_ID_field_xpath).send_keys(user_ID)
        
        password_field_xpath = '//*[@id="idPassword"]'
        driver.find_element(By.XPATH, password_field_xpath).send_keys(password)

        signin_button_xpath = '//*[@id="btn_login"]'
        driver.find_element(By.XPATH, signin_button_xpath).click()
        
        return driver


    def __catalog_loop(self, driver: webdriver.Firefox, SFA_Reports_Xpaths: dict):
       for files, xpaths in SFA_Reports_Xpaths.items():
                if self.weekday != 0 and files == 'Onward 6P by Date':
                    continue
                Export_Xpath = '//*[@id="menuoptionCell_Export"]/img'
                data_xpath = '//*[@id="menuOptionItem_Data"]'
                csv_css_selector = '#menuOptionItem_CSV > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)'
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, xpaths))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, Export_Xpath))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, data_xpath))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, csv_css_selector))).click()

                download_finished_xpath = '/html/body/div[5]/div/table/tbody[1]/tr/td/div[3]/a[1]'
                time.sleep(5)
                if files == 'Warranty Registrations for SFDC updates':
                    time.sleep(120)
                WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.XPATH, download_finished_xpath))).click()
                time.sleep(3)
        
                if self.weekday == 0:
                
                    driver.get(r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2Fcc%20Service%20Parts%2FAnakkar%2FOnward%20Att.%20Rate%2FOnward%20Accessories%20-%202023%20Attachment%20Rate')
                    export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
                    WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()
                    excel_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[2]/table'
                    driver.find_element(By.XPATH, excel_xpath).click()
                    
                    download_finished_xpath = '/html/body/div[5]/div/table/tbody[1]/tr/td/div[3]/a[1]'
                    time.sleep(5)



    def navigate_catalog(self):
        driver = self.OBI_Login()
        driver.get("http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?catalog")
        # First folder path is to SFA Reports, second is to CC Service Parts.
        # The array embedded in folder_paths_xpaths goes from CC Service Parts -> Annakar -> Onward Att. Rate
        Shared_Folders_Xpath = '/html/body/div[2]/div/table[1]/tbody/tr/td[2]/div/table[1]/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/span/span/span'
        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, Shared_Folders_Xpath))).click()
        SFA_Reports_Xpath = '/html/body/div[2]/div/table[1]/tbody/tr/td[2]/div/table[1]/tbody/tr/td[2]/div/div/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[86]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/a'
        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, SFA_Reports_Xpath))).click()

        SFA_Reports = {'Onward 6P by Date' : '//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[6]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Order Details for WR CY':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[8]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Plan ETL - Objectives Data':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[9]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Plan ETL - Plan Data':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[10]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Warr Reg Flag CY':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[14]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Warranty Accepted Amount CY for SFDC updates':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[15]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a',
                       'Warranty Registrations for SFDC updates':'//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[16]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a'       }
        
        try:
            for files, xpaths in SFA_Reports.items():
                if self.weekday != 0 and files == 'Onward 6P by Date':
                    continue
                Export_Xpath = '//*[@id="menuoptionCell_Export"]/img'
                data_xpath = '//*[@id="menuOptionItem_Data"]'
                csv_css_selector = '#menuOptionItem_CSV > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)'
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, xpaths))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, Export_Xpath))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, data_xpath))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, csv_css_selector))).click()

                download_finished_xpath = '/html/body/div[5]/div/table/tbody[1]/tr/td/div[3]/a[1]'
                time.sleep(5)
                if files == 'Warranty Registrations for SFDC updates':
                    time.sleep(120)
                WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.XPATH, download_finished_xpath))).click()
                time.sleep(3)
        
            if self.weekday == 0:
                
                driver.get(r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2Fcc%20Service%20Parts%2FAnakkar%2FOnward%20Att.%20Rate%2FOnward%20Accessories%20-%202023%20Attachment%20Rate')
                export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()
                excel_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[2]/table'
                driver.find_element(By.XPATH, excel_xpath).click()
                
                download_finished_xpath = '/html/body/div[5]/div/table/tbody[1]/tr/td/div[3]/a[1]'
                time.sleep(5)
        except TimeoutException:
            time.sleep(60)
            self.__catalog_loop(driver, SFA_Reports)
        
        self.__catalog_loop(driver, SFA_Reports)
        
        print("Catalog downloaded!")
        driver.close()
        driver.quit()
        return None
            



    def download_files(self):
        """This function takes the driver from the OBI Login and then checks the day of the week to determine
        what files need to be downloaded. There are two lists of URLs. The first list is for files ONLY on Mondays
        The second list is for files on Thursdays. All Thursday files are downloaded Monday as well"""
    
        driver = self.OBI_Login()

        day_of_week = self.weekday[0]

        New_Reference_Data_URL = ''


        Onward_6Pby_date_new_xpath = '//*[@id="idCatalogItemsAccordion"]/div[1]/div[2]/table/tbody/tr[6]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[5]/a'

        attachment_rate_urls = [r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FOnward%206P%20by%20date',
                                    r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2Fcc%20Service%20Parts%2FAnakkar%2FOnward%20Att.%20Rate%2FOnward%20Accessories%20-%202023%20Attachment%20Rate']

        reference_data_urls = [r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FPLAN%20ETL%20-%20Objectives%20Data',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FPLAN%20ETL%20-%20Plan%20Data',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarr%20Reg%20Flag%20CY',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarranty%20Accepted%20Amount%20CY%20for%20SFDC%20updates',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarranty%20Registrations%20for%20SFDC%20updates',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FOrder%20-%20Details%20for%20WR%20CY']

        
        if day_of_week == 0:
            for URL in attachment_rate_urls:
                
                driver.get(URL)
                export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'

                WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()

                if 'Anakkar' in URL:
                    excel_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[2]/table'
                    driver.find_element(By.XPATH, excel_xpath).click()

                else:
                    data_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[5]/table/tbody/tr/td[2]'
                    driver.find_element(By.XPATH, data_xpath).click()
                    csv_xpath = '/html/body/div[4]/table/tbody/tr[1]/td[1]/a[2]/table/tbody/tr/td[2]'
                    driver.find_element(By.XPATH, csv_xpath).click()
                time.sleep(5)
        try:
            for URL in reference_data_urls:
                driver.get(URL)
                export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
                WebDriverWait(driver, 120).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()
                data_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[5]/table/tbody/tr/td[2]'          
                driver.find_element(By.XPATH, data_xpath).click()
                csv_xpath = '/html/body/div[4]/table/tbody/tr[1]/td[1]/a[2]/table/tbody/tr/td[2]'
                driver.find_element(By.XPATH, csv_xpath).click()
                if 'regis' in URL.lower():
                    print('Registration!!')
                    time.sleep(30)
                    print('Done sleeping!')
                time.sleep(5)

        except TimeoutException:
            current_position = reference_data_urls.index(URL)
            print("Timed out!")
            print("Trying again!")
            time.sleep(600)
            for num in range(current_position, len(reference_data_urls)-1):
                URL = reference_data_urls[num]
                driver.get(URL)
                export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
                WebDriverWait(driver, 120).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()
                data_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[5]/table/tbody/tr/td[2]'          
                driver.find_element(By.XPATH, data_xpath).click()
                csv_xpath = '/html/body/div[4]/table/tbody/tr[1]/td[1]/a[2]/table/tbody/tr/td[2]'
                driver.find_element(By.XPATH, csv_xpath).click()
                if 'regis' in URL.lower():
                    print('Registration!!')
                    time.sleep(15)
                    print('Done sleeping!')
                time.sleep(5)


        print('Loop end!')
        driver.close()
        driver.quit()
        print("Driver Quit!")
        return None

    def check_files_downloaded(self):
        """This function conducts an error check to ensure all files required are downloaded.
        If there are files missing then the next function redownloads them"""
        
        day_of_week = self.weekday[0]
        if day_of_week not in (0,3):
            print('Not a Monday or Thursday, come back then!')
            return None

        print(f'Day of week is {day_of_week}')
        attachment_rate_urls = [r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FOnward%206P%20by%20date',
                                    r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2Fcc%20Service%20Parts%2FAnakkar%2FOnward%20Att.%20Rate%2FOnward%20Accessories%20-%202023%20Attachment%20Rate']

        reference_data_urls = [r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FPLAN%20ETL%20-%20Objectives%20Data',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FPLAN%20ETL%20-%20Plan%20Data',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarr%20Reg%20Flag%20CY',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarranty%20Accepted%20Amount%20CY%20for%20SFDC%20updates',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FWarranty%20Registrations%20for%20SFDC%20updates',
                                r'http://ccinsight.internal.clubcar.com:9502/analytics/saw.dll?PortalGo&Action=prompt&path=%2Fshared%2FSFA%20Reports%2FOrder%20-%20Details%20for%20WR%20CY']

        attachment_rate_dict = {0:'Onward 6P by date.csv', 1: 'Onward Accessories - 2023 Attachment Rate.xlsx'}
        reference_data_dict = {0:'PLAN ETL - Objectives Data.csv', 1:'PLAN ETL - Plan Data.csv', 2: 'Warr Reg Flag CY.csv', 3: 'Warranty Accepted Amount CY for SFDC updates.csv', 4:'Warranty Registrations for SFDC updates.csv', 5: 'Order - Details for WR CY.csv'}

        downloads = os.listdir(r'C:\Users\wxm3287\Downloads')
        csvs_xlsxs = [file for file in downloads if '.csv' in file or '.xlsx' in file]
    
        
        reference_data_missed_urls = [reference_data_urls[position] for position, file in reference_data_dict.items() if file not in csvs_xlsxs]
        print('Created missing list! ')
        if day_of_week == 0:
            attachment_rate_missed_urls = [attachment_rate_urls[position] for position, file in attachment_rate_dict.items() if file not in csvs_xlsxs]
            missed_urls = attachment_rate_missed_urls + reference_data_missed_urls
        
        else:
            missed_urls = reference_data_missed_urls
        
        print(f'Sending missing list! There is {len(missed_urls)} missing files!')

        return missed_urls

    def download_missed_files(self):
        """This function checks to see if any files were missed while downloading. If there are none, it terminates and the 
        next part of the program begins"""
        try:
            missed_urls = self.check_files_downloaded()
            print(f'Checked Downloads Folder! There is {len(missed_urls)} missing files!')
            if len(missed_urls) == 0:
                return None  
        except TypeError:
            return None


        driver = self.OBI_Login()      

        for URL in missed_urls:
            driver.get(URL)
            export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
            WebDriverWait(driver, 300).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()

            if 'Anakkar' in URL:
                    excel_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[2]/table'
                    driver.find_element(By.XPATH, excel_xpath).click()

            else:
                data_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[5]/table/tbody/tr/td[2]'
                driver.find_element(By.XPATH, data_xpath).click()
                csv_xpath = '/html/body/div[4]/table/tbody/tr[1]/td[1]/a[2]/table/tbody/tr/td[2]'
                driver.find_element(By.XPATH, csv_xpath).click()
        

            time.sleep(30)
        driver.quit()
        return None

    def login_download_check_redownload(self):
        self.OBI_Login()
        self.download_files()
        print('First Sweep Done!')
        self.check_files_downloaded()
        self.download_missed_files()



def move_and_rename_files(weekday):
    """This function takes the current files and moves them to their desginated location in the 'K' drive
    One file needs to be renamed every Monday and that file alone will be renamed with the current date in 
    YYYY-MM-DD format."""
    day_of_week, current_date = weekday

    attachment_rate_dict = {0:'Onward 6P by date.csv', 1: 'Onward Accessories - 2023 Attachment Rate.xlsx'}
    reference_data_dict = {0:'PLAN ETL - Objectives Data.csv', 1:'PLAN ETL - Plan Data.csv', 2: 'Warr Reg Flag CY.csv', 3: 'Warranty Accepted Amount CY for SFDC updates.csv', 4:'Warranty Registrations for SFDC updates.csv', 5: 'Order - Details for WR CY.csv'}
        
    for position, reference_data_dict in reference_data_dict.items():
        shutil.move(rf'C:\Users\wxm3287\Downloads\{reference_data_dict}', rf'\\AGS-US-303\Specdata\Analytics_Reports\Reference Data\{reference_data_dict}')
    
    if day_of_week == 0:
        filename = r'C:\Users\wxm3287\Downloads\Onward Accessories - 2023 Attachment Rate.xlsx'

        basename, extension = os.path.splitext(filename)

        new_filename = f'{basename} {current_date}{extension}'


        os.rename(filename, new_filename)

        slice_begin = new_filename.rfind('\\')
        onward_accessories = new_filename[slice_begin+1:]
        
        attachment_rate_dict[1] = onward_accessories

        for position, attachment_rate_file in attachment_rate_dict.items():
            shutil.move(rf'C:\Users\wxm3287\Downloads\{attachment_rate_file}', rf'K:\Analytics_Reports\Reference Data\AttachmentRate\{attachment_rate_file}')

    print('Files moved :)')
    return None



def download_files_from_OBI(weekday):
    get_files = DownloadFilesfromOBI(weekday)
    get_files.download_files()
    get_files.download_missed_files()




def all_together_now():
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



all_together_now()

