import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.wait import WebDriverWait

from OBI_Downloads import DownloadFilesfromOBI


class Check_Downloads(DownloadFilesfromOBI):
     
    def __init__(self, weekday) -> None:
        super().__init__(weekday=weekday)
        self.weekday = weekday

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
        if day_of_week == 0:
            attachment_rate_missed_urls = [attachment_rate_urls[position] for position, file in attachment_rate_dict.items() if file not in csvs_xlsxs]
            missed_urls = attachment_rate_missed_urls + reference_data_missed_urls
        
        else:
            missed_urls = reference_data_missed_urls
    

        return missed_urls


    def download_missed_files(self):
        """This function checks to see if any files were missed while downloading. If there are none, it terminates and the 
        next part of the program begins"""
        missed_urls = self.check_files_downloaded()
        if len(missed_urls) == 0:
            return None  
      
        driver = self.OBI_Login()      

        for URL in missed_urls:
            driver.get(URL)
            export_xpath = '/html/body/div[2]/div/table[1]/tbody/tr[1]/td[2]/div/table[1]/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td[7]'
            WebDriverWait(driver, 300).until(expected_conditions.element_to_be_clickable((By.XPATH, export_xpath))).click()

            data_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[5]/table/tbody/tr/td[2]'
            driver.find_element(By.XPATH, data_xpath).click()
            csv_xpath = '/html/body/div[4]/table/tbody/tr[1]/td[1]/a[2]/table/tbody/tr/td[2]'
            driver.find_element(By.XPATH, csv_xpath).click()

            if 'Anakkar' in URL:
                    excel_xpath = '/html/body/div[3]/table/tbody/tr[1]/td[1]/a[2]/table'
                    driver.find_element(By.XPATH, excel_xpath).click()

            time.sleep(30)

        driver.quit()
        return None

    def login_download_check_redownload(self):
        self.OBI_Login()
        self.download_files()
        self.check_files_downloaded()
        self.download_missed_files()