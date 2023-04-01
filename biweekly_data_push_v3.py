from time import sleep, time
import datetime
import shutil
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService


"""The purpose of this program is to download multiple files from Oracle Business Intelligence and place
the files into the appropriate folder in the 'K' Drive. This is done by webcrawling using Selenium 
for now and will later be changed to ODBC access or API access."""

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
    
    return day_of_week, today_str



def OBI_Login():
    """This function starts Selenium / Webcrawling and logins into Oracle Business Inelligence. 
    It uses the current users login info to achieve this. This needs to be changed in the future to a 
    generic user such as the system Admin"""
    day_of_week = day_of_week_check()[0]
   
    if day_of_week not in (0,3):
        print('Not a Monday or Thursday, come back then!')
        return None


    user_ID = ''.upper()
    password = ''
    login_URL = r'http://ccinsight.internal.clubcar.com:9502/bi-security-login/login.jsp?msi=false&redirect=L2FuYWx5dGljcy9zYXcuZGxsP2JpZWVob21lJnN0YXJ0UGFnZT0xJmhhc2g9ajdETVBqQkk2N2l4NHBQbU1FTURnbmNhTGZmai00NmRDOVRKMUlmdzBfTkdWdHpzLWs3YjJQSkJrZDJ6QUc1Yg=='

    quiet = Options()
    quiet.add_argument('-headless')

    driver = webdriver.Firefox(options=quiet, service=FirefoxService(r'/home/usacys/Desktop/Paul/geckodriver'))
    driver.get(login_URL)
    
    user_ID_field_xpath ='//*[@id="idUser"]'
    
    WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, user_ID_field_xpath))).click()
    driver.find_element(By.XPATH, user_ID_field_xpath).send_keys(user_ID)
    
    password_field_xpath = '//*[@id="idPassword"]'
    driver.find_element(By.XPATH, password_field_xpath).send_keys(password)

    signin_button_xpath = '//*[@id="btn_login"]'
    driver.find_element(By.XPATH, signin_button_xpath).click()
    
    return driver

def download_files():
    """This function takes the driver from the OBI Login and then checks the day of the week to determine
    what files need to be downloaded. There are two lists of URLs. The first list is for files ONLY on Mondays
    The second list is for files on Thursdays. All Thursday files are downloaded Monday as well"""
   
    driver = OBI_Login()

    day_of_week = day_of_week_check()[0]

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
            sleep(5)

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
            sleep(15)
            print('Done sleeping!')
        sleep(5)
    
    print('Loop end!')
    driver.quit()
    return None

def check_files_downloaded():
    """This function conducts an error check to ensure all files required are downloaded.
     If there are files missing then the next function redownloads them"""
    
    day_of_week = day_of_week_check()[0]
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


def download_missed_files():
    """This function checks to see if there are files downloaded. If there are none, it terminates and the 
    next part of the program begins"""
    try:
        missed_urls = check_files_downloaded()
        print(f'Checked Downloads Folder! There is {len(missed_urls)} missing files!')  
    except TypeError:
        return None


    driver = OBI_Login()      

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
       

        sleep(30)
    driver.quit()
    return None

def move_and_rename_files():
    """This function takes the current files and moves them to their desginated location in the 'K' drive
    One file needs to be renamed every Monday and that file alone will be renamed with the current date in 
    YYYY-MM-DD format."""
    day_of_week, current_date = day_of_week_check()

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

def all_together_now():
    """This function acts as the Main() function would in a C program. Or at least a rudimentary 
    version of the Main() function. This combines all previous functions and runs the program
    Later there will be an associated text document with this program that will keep track of unsuccessful
    vs successful runs"""
    download_files()
    print('First Sweep Done!')
    print(datetime.datetime.now())
    download_missed_files()
    print('Files Downloaded!')
    move_and_rename_files()
    return ":)"

start_time = time()
current_time = datetime.datetime.now()
print(current_time)
all_together_now()

print(f'Program completed in {(time()-start_time)/60} minutes!')
print(datetime.datetime.now())
