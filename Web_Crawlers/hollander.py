"""Car part webcrawler. 
This is the Hollander module. This has been upgraded and slimmed down by removing classes that did not accomplish the functions for the hollander module.
This webcrawler has 3 primary goals. 
Goal 1) scrape information from all car parts websites
Goal 2) Match that information to all parts to a car based upon year, make, and model
Goal 3) Create a map that shows where all the parts are geographically located
Goal 4) Color code the parts based upon their function. E.g. Yellow for electrical components, 
    Red for cosmetic, blue for fluid management, etc.

Note: in the future to reduce amount of retries it will be wise to write the html to a text file and 
then read from that page for experimentation

URL Example:hollanderparts.com/used-auto-parts/Year/Make/Model/Category /Part Type      /Fitment
https://www.hollanderparts.com/used-auto-parts/2007/honda/crv/electrical/601-alternator/601-50108-get-parts
"""

from requests import get
from time import sleep
from fuzzywuzzy import fuzz
from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService


class hollander:
    """The purpose of the search bar is to give the user to search easily through hollanders database of parts
        and find the part they are looking for based upon one of 7 options the culmination of this is found in the
        search bar function"""
    def __init__(self, year: int, make: str, model: str):
        self.year: int = year
        self.make: str = make
        if self.make.lower() == 'chevy':
            self.make = 'Chevrolet'
        self.model: str = model
        self.get_counter: int = 0
  
    def bypass_cookies(self, URL):
        # Get past the cookie wall on Hollanders webpage
        quiet = Options()
        quiet.headless = True
        try:
            driver = webdriver.Firefox(options=quiet, service=FirefoxService(r'/home/usacys/Desktop/Paul/geckodriver'))
        except WebDriverException:
            driver = webdriver.Firefox(options=quiet, service=FirefoxService(r"C:\Users\Michel´s PC\Desktop\Paul\geckodriver"))
        driver.get(URL)
        self.get_counter +=1
        x_path = r'//*[@id="onetrust-accept-btn-handler"]'
        sleep(1)
        WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.XPATH, x_path))).click()
        return driver

    def webpage_sorting(self, URL: str, selection=None, zip_code=None):
        # Pick your sorting method options are listed below
        print("""Pick your sorting method by the number below:
                    "1": "Price (Lowest to Highest)",
                    "2": "Price (Highest to Lowest)",
                    "3": "Condition (Very Good to ",
                    "4": "Condition (Fair to Very ",
                    "5": "Mileage (Lowest to Highest)",
                    "6": "Mileage (Highest to Lowest)", 
                    "7": "Location (Nearest to Me)""")
        u_select = input('Enter your preference by number or type "no" or "quit" to quit.').lower()
        if u_select == '7':
            u_select = '8'
            if zip_code == None:
                u_zip_code = input('What is your zip code?')
                zip_code = u_zip_code


        if u_select[0] == 'n' or u_select[0] == 'q':
            return None

        else:
            selection = u_select
        driver = self.bypass_cookies(URL)
        sleep(3)
        if selection == "8":
            location_bar = WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.ID, "txtPostalCode")))
            location_bar.send_keys(zip_code)
       
        WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.ID, "lstSortOrdinal")))
        select = Select(driver.find_element(By.ID, "lstSortOrdinal"))
        select.select_by_value(selection)
        sleep(5)
        return driver.page_source


    def get_categories(self):
        """Get all categories for your vehicle. E.g. for 2007 Honda C-RV the categories would be:
        Accessories, Air and Fuel, Axle, Brakes, Center Body, Cooling and Heating, Doors, Electrical, 
        Engine, Engine Accessories, Entertainment, Front Body, Glass and Mirrors, Interior, Lights, 
        Miscellaneous, Rear Body, Safety, Suspension-Steering, Transmission ,Wheels"""

        URL = f'https://www.hollanderparts.com/used-auto-parts/{self.year}/{self.make}/{self.model}'
        part_cat_parser = BeautifulSoup(get(URL).text, 'html.parser')
        self.get_counter += 1
        part_category_list = []
        for part in part_cat_parser.find_all('div', 'ymmSelection'):
            if isinstance(part, type(None)):
                pass
            else:
                for part_string in part.stripped_strings:                 
                    part_category_list.append(part_string.lower())
        return part_category_list


    def get_part_subcategories(self):
        """Get list of part subcategories E.g. if the category selected was Electrical:AC Wire Harness,
        Alternator, Antenna, Audio Equipment Radio, Automatic Headlamp Dimmer, Backup Light, Battery,
        Battery Tray, Blower Motor, Body Wire Harness, Camera/Projector"""
        
        master_subcat_list = []

        for part_category in self.get_categories():
            URL = f'https://www.hollanderparts.com/used-auto-parts/{self.year}/{self.make}/{self.model}/{part_category}'
            part_sub_cat_parser = BeautifulSoup(get(URL).content, 'html.parser')
            self.get_counter += 1
            part_sub_cat_avail = part_sub_cat_parser.find_all('div', 'ymmSelection')
        
            dirty_cat_subcat_list = []
            clean_cat_subcat_list = []
            cat_subcat_dict= {}
            for parse in part_sub_cat_avail:
                sub_cat_info = parse.find('a', href= True)
                sub_cat = sub_cat_info.text
                clean_cat_subcat_list.append(sub_cat)
                sub_cat_url = sub_cat_info['href']
                dirty_cat_subcat_list.append(sub_cat_url)
            
            cat_subcat_dict['Clean'] = clean_cat_subcat_list
            cat_subcat_dict['Dirty'] = dirty_cat_subcat_list
            master_subcat_list.append({part_category:cat_subcat_dict})
            
        return master_subcat_list


    # Year > Make > Model > Category > Part Type > Fitment
    def get_part_fitment(self, part: str):
        """This gives the next to last URL where the parts actually are. Fitment typically has only one result but
        at times more than one option will be available"""
        
        part = part.lower()
        part_match_list = []
        for category_info in self.get_part_subcategories():
            for category, info_dict in category_info.items():
                clean_list: list = info_dict['Clean']
                url_list: list = info_dict['Dirty']
                for clean, url in zip(clean_list, url_list):
                    text_match = fuzz.ratio(part, clean.lower())
                    if part == clean.lower():
                        return url
                    elif text_match > 50:
                        part_match_list.append({'Display':clean,'URL': url, 'Match Ratio': text_match})
        highest_ratio = sorted(part_match_list, key= lambda x: x['Match Ratio'])
        part_counter = count()
        display_matches = [(part_counter.__next__() +1, match['Display']) for match in highest_ratio]

        if len(highest_ratio) == 1:
            URL = f"https://www.hollanderparts.com/{highest_ratio[0]['URL']}"
        if len(highest_ratio) == 0:
            return 'No fitment found'

        else:
            print(display_matches)
            user_part_choice = input("""Select your part by the number next to it. If your part is not present, type no or quit to quit""").lower()

        if user_part_choice[0] == 'n' or user_part_choice[0] == 'q':
            return None
        else:
            URL = f"https://www.hollanderparts.com/{highest_ratio[int(user_part_choice)-1]['URL']}"
        fitment_page = BeautifulSoup(get(URL).content, 'html.parser')  
        self.get_counter +=1
        fitment_parse = fitment_page.find_all('div', class_ = 'ymmSelection')
        fitment_match_list = []
        for fitment_refined in fitment_parse:
            fitment_info = fitment_refined.find('a', href= True)
            fitment_url = fitment_info['href']
            fitment = fitment_info.text
            fitment_match_list.append({'Display':fitment,'URL': fitment_url})
        if len(fitment_match_list) == 0:
            return fitment_match_list[0]
        fitment_counter = count()
        fitment_display = [(fitment_counter.__next__() +1, match['Display']) for match in fitment_match_list]
        print(fitment_display)
        user_fitment_choice = input("""Select your part fitment by the number next to it. If your part is not present, type no or quit to quit""").lower()
        if user_fitment_choice[0] == 'n' or user_part_choice[0] == 'q':
            return None
        else:
            return fitment_match_list[int(user_fitment_choice)-1]

    
    def get_parts(self, part: str, selection = None, zip_code=None):
        # The culiminating search bar that lets the user search for parts and sort their results
        try:
            fitment = self.get_part_fitment(part)
            url_end = fitment['URL']
        except TypeError:
            return fitment

        URL = f'https://www.hollanderparts.com/{url_end}'
        part_page = self.webpage_sorting(URL, selection, zip_code)
        
        part_parser = BeautifulSoup(part_page, 'html.parser')
        
        No_parts = part_parser.find('div', class_="title")
        if No_parts != None:
            return 'No Parts Found'



        part_avail = part_parser.find_all('div', 'individualPartHolder')

        part_d_list =[]

        for part_tag in part_avail:
            part_dict = {}
            price_text = part_tag.find('div', class_='partPrice').text
            if price_text[-5].isnumeric():
                price = float(price_text[-5:])
            else:
                price = price_text
            
            part_dict['Price']= price


            grade = part_tag.find('div', class_='gradeText').text
        
        
            try:
                shipping = part_tag.find('div', class_='partShipping').text
                if shipping[-5].isnumeric():
                    shipping_price = float(shipping[-5:])
                else:
                    shipping_price = shipping
                part_dict['Shipping'] = shipping_price
            except AttributeError:
                part_dict['Shipping'] = 'Call for Price'
            
            info = part_tag.find('a', href=True)
            more_info = info['href']
            miles_org_locate = part_tag.find_all('div', class_='location')
            
            miles_text = miles_org_locate[0].text
            miles_begin = miles_text.index('Mileage') + len('Mileage') + 1
            miles_replace = miles_text[miles_begin:].replace(',','')
            miles = int(miles_replace)
            

            organization = miles_org_locate[1].text
            location = miles_org_locate[2].text


            
            part_dict['Price']= price
            part_dict['Grade'] = grade.strip()
            part_dict['Mileage'] = miles
            part_dict['Organization'] = organization.strip()
            part_dict['Location'] = location.strip()
            part_dict['More Info'] = f'https://www.hollanderparts.com{more_info}'
 
            
            part_d_list.append(part_dict)

        return part_d_list

 





