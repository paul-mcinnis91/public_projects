from requests import get
from time import sleep
from itertools import count
import sys

from src import local_data_pull
from src.user_interactions import User_Interface

from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService


class Hollander:
    """The purpose of the search bar is to give the user to search easily through hollanders database of parts
        and find the part they are looking for based upon one of 7 options the culmination of this is found in the
        search bar function"""
    
    def __init__(self, year: str, make: str, model: str):
        self.year: str = year
        self.make: str = make.lower()
        self.model: str = model.lower()
        self.get_counter: int = 0
        self.user_interface = User_Interface()


    def _bypass_cookies(self, URL: str) -> webdriver.Firefox:
        """Interacts with the accept cookies button so the program can get past the cookies to get
        to the HTML data in the back ground.
        
        Args: URL (str) the final URL where the cookies need to be bypassed.
        
        Returns: driver (webdriver.Firefox) the selenium object to navigate the webpage and press 
        buttons"""
        quiet = Options()
        quiet.headless = True
        geckodriver_directory = local_data_pull.get_top_level_directories("geckodriver")
        driver = webdriver.Firefox(options=quiet, service=FirefoxService(geckodriver_directory))
        driver.get(URL)

        self.get_counter +=1
        x_path = r'//*[@id="onetrust-accept-btn-handler"]'
        sleep(1)
        WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.XPATH, x_path))).click()
        return driver

    def _webpage_sorting(self, URL: str, selection: str = None, zip_code: str = None):
        """Sorts the data to the preference of the user. Will probably eliminate this in the future.
        
        Args: URL (str) the webpage to navigate to.
              selection (str) 1-6, 8 each one giving the user a set of options:
                    "1": "Price (Lowest to Highest)",
                    "2": "Price (Highest to Lowest)",
                    "3": "Condition (Very Good to ",
                    "4": "Condition (Fair to Very ",
                    "5": "Mileage (Lowest to Highest)",
                    "6": "Mileage (Highest to Lowest)", 
                    "8": "Location (Nearest to Me)

              zip_code (str) the user's zip code
        
        Returns: driver.page_source (str) the HTML string data from the webpage.
              """
        print("""Pick your sorting method by the number below:
                    "1": "Price (Lowest to Highest)",
                    "2": "Price (Highest to Lowest)",
                    "3": "Condition (Very Good to ",
                    "4": "Condition (Fair to Very ",
                    "5": "Mileage (Lowest to Highest)",
                    "6": "Mileage (Highest to Lowest)", 
                    "8": "Location (Nearest to Me)""")
        
        selection = input('Enter your preference by number or type "no" or "quit" to quit.').lower()

        driver = self._bypass_cookies(URL)
        sleep(3)

        if selection == "8":
            location_bar = WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.ID, "txtPostalCode")))
            location_bar.send_keys(zip_code)
       
        WebDriverWait(driver, 40).until(expected_conditions.element_to_be_clickable((By.ID, "lstSortOrdinal")))
        select = Select(driver.find_element(By.ID, "lstSortOrdinal"))
        select.select_by_value(selection)

        sleep(5)
        return driver.page_source

    def _get_part_category_list(self, parsed_car_parts: list) -> list:
        """Takes list of parsed_car_parts and refines the car part categories then returns it
        
        Args: parsed_car_parts (list) return from beautiful soup find all method
        
        Returns part_category_list (list) list of refined car parts"""

        part_category_list = []
        for part in parsed_car_parts:
            if isinstance(part, type(None)):
                pass
            
            part_strings = list(part.stripped_strings)
            part_category_list.extend(part_strings)
        
        lower_cased_parts = [part.lower() for part in part_category_list]
        return lower_cased_parts

    def _get_categories(self):
        """Get all categories for your vehicle. E.g. for 2007 Honda C-RV the categories would be:
        Accessories, Air and Fuel, Axle, Brakes, Center Body, Cooling and Heating, Doors, Electrical, 
        Engine, Engine Accessories, Entertainment, Front Body, Glass and Mirrors, Interior, Lights, 
        Miscellaneous, Rear Body, Safety, Suspension-Steering, Transmission, Wheels"""

        URL = f'https://www.hollanderparts.com/used-auto-parts/{self.year}/{self.make}/{self.model}'
        part_cat_parser = BeautifulSoup(get(URL).text, 'html.parser')
        self.get_counter += 1
        part_category_list = part_cat_parser.find_all('div', 'ymmSelection')
        refined_part_list = self._get_part_category_list(part_category_list)
        return refined_part_list
            

    def _get_full_urls(self, part_category: str, parse_subcats: list) -> dict:
        """Takes the parse_subcats list and pulls out all the different URLs and their 
        titles to create a dictionary of lists that can be queried later. 
        The dictionaries have two lists within. The key to each dictionary is part_category.

        This needs some serious redesign...
        
        Args: parse_subcats: list that is returned from beautiful soup find all on the part category page
                of hollanderparts.com
                
        Returns: dcitionary of lists of all subcategories available and their URLs"""


        dirty_cat_subcat_list = []
        clean_cat_subcat_list = []
        cat_subcat_dict = {}
        for parse in parse_subcats:
            sub_cat_info = parse.find('a', href= True)
            sub_cat = sub_cat_info.text
            clean_cat_subcat_list.append(sub_cat)
            sub_cat_url = sub_cat_info['href']
            dirty_cat_subcat_list.append(sub_cat_url)

        cat_subcat_dict['Part Categories'] = clean_cat_subcat_list
        cat_subcat_dict['Part Category URLs'] = dirty_cat_subcat_list

        return {part_category:cat_subcat_dict}

        

    def _get_part_subcategories(self):
        """Get list of part subcategories E.g. if the category selected was Electrical:AC Wire Harness,
        Alternator, Antenna, Audio Equipment Radio, Automatic Headlamp Dimmer, Backup Light, Battery,
        Battery Tray, Blower Motor, Body Wire Harness, Camera/Projector"""
        
        master_subcat_list = []

        for part_category in self._get_categories():
            URL = f'https://www.hollanderparts.com/used-auto-parts/{self.year}/{self.make}/{self.model}/{part_category}'
            part_sub_cat_parser = BeautifulSoup(get(URL).content, 'html.parser')
            self.get_counter += 1
            part_sub_cat_avail = part_sub_cat_parser.find_all('div', 'ymmSelection')

            url_dictionary = self._get_full_urls(part_category, part_sub_cat_avail)
            master_subcat_list.append(url_dictionary)
            
        return master_subcat_list



    def _create_fitment_match_list(self, fitment_parse_matches: list) -> list:
        """Private function called upon in get_part_fitment to create list of fitment matches
        
        Args: fitment_parse_matches (list) return from beautiful soup.find_all function for fitment info
        
        Returns: list of dictionaries with more refined information"""

        fitment_match_list = []
        for fitment_refined in fitment_parse_matches:
            fitment_info = fitment_refined.find('a', href= True)
            fitment_url = fitment_info.get('href')
            fitment = fitment_info.text
            fitment_match_list.append({'Display':fitment,'URL': fitment_url})
        
        return fitment_match_list
    
    def _get_part_fitment_matches(self, part_subcat_list: list, part: str) -> list:
        """Iterates through the part_subcat_list and refines the list further
        
        Args: part_subcat_list (list) list of part subcategories
        
        Returns list of refined subcategories
        
        Example part_subcat_list 
        [{'Brakes':{'Part Categories: [Front Brakes, Back Brakes], 
                    Part Category URLs: [hollander.com/front_brakes, hollander.com/back_brakes]}]"""

        part_match_list = [part_subcat_dict 
                           for part_subcat_dict 
                           in part_subcat_list 
                           if fuzz.ratio(part, 
                                         part_subcat_dict.get("Part Categories"))]
        
        return part_match_list
    # Year > Make > Model > Category > Part Type > Fitment


    def _get_part_fitment(self, part: str) -> dict:
        """This gives the next to last URL where the parts actually are. Fitment typically has only one result but
        at times more than one option will be available"""
        
        part = part.lower()
        part_subcategories = self._get_part_subcategories()
        print(part_subcategories)
        part_match_list = self._get_part_fitment_matches(part_subcategories, part)

        highest_ratio = sorted(part_match_list, key= lambda x: x['Match Ratio'])
        part_counter = count()
        display_matches = [(part_counter.__next__() +1, match['Display']) for match in highest_ratio]

        if len(highest_ratio) == 1:
            URL = f"https://www.hollanderparts.com/{highest_ratio[0]['URL']}"

        else:
            user_part_choice = self.user_interface.user_input_matches(display_matches) - 1
            URL = f"https://www.hollanderparts.com/{highest_ratio[int(user_part_choice)].get(URL)}"


        fitment_page = BeautifulSoup(get(URL).content, 'html.parser')  
        self.get_counter +=1
        fitment_parse = fitment_page.find_all('div', class_ = 'ymmSelection')
        fitment_match_list = self._create_fitment_match_list(fitment_parse)
        
        fitment_counter = count()
        fitment_display = [(fitment_counter.__next__() +1, match['Display']) for match in fitment_match_list]
        user_fitment_choice = self.user_interface.user_input_matches(fitment_display) - 1
        
        return fitment_match_list[int(user_fitment_choice)]

    def _price_slicer(self, price_text: str) -> str:
        """Takes the price text and checks to see if there is numbers in the end of it. 
        If there is, cuts it out and returns that. Otherwise returns the full price text.
        
        Args: price_text (str) string the string with the price inside of it
        
        Returns: the price string either shortened or the same."""

        if price_text[-5].isnumeric():
            price = price_text[-5:]
            return price
        
        return price



    def get_parts(self, part: str, selection = None, zip_code=None) -> list:
        """Pick your sorting method by the number below:
                    "1": "Price (Lowest to Highest)",
                    "2": "Price (Highest to Lowest)",
                    "3": "Condition (Very Good to ",
                    "4": "Condition (Fair to Very ",
                    "5": "Mileage (Lowest to Highest)",
                    "6": "Mileage (Highest to Lowest)", 
                    "8": "Location (Nearest to Me)"""
        # The culiminating search bar that lets the user search for parts and sort their results

        part = part.lower()
        fitment = self._get_part_fitment(part)
        url_end = fitment.get("URL")

        if isinstance(url_end, type(None)):
            sys.exit("Fitment Information not found")
     

        URL = f'https://www.hollanderparts.com/{url_end}'
        part_page = self._webpage_sorting(URL, selection, zip_code)
        
        part_parser = BeautifulSoup(part_page, 'html.parser')
        
        No_parts = part_parser.find('div', class_="title")
        if No_parts != None:
            sys.exit("No Parts Found")

        part_avail = part_parser.find_all('div', 'individualPartHolder')

        part_d_list =[]

        for part_tag in part_avail:
            part_dict = {}
            price_text = part_tag.find('div', class_='partPrice').text
            price = self._price_slicer(price_text)
            
            part_dict['Price']= price


            grade = part_tag.find('div', class_='gradeText').text
        
           
            shipping = part_tag.find('div', class_='partShipping').text
            shipping_price = self._price_slicer(shipping)
            part_dict['Shipping'] = shipping_price
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

 





