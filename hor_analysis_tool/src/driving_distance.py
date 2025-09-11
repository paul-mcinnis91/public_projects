#!/usr/bin/env python3
from datetime import timedelta
import pandas as pd
import googlemaps as gm
from src import helper
 

class Driving_Distance:
    def __init__(self, hor_csv_path: str):
        self.hor_csv_path: str = hor_csv_path
        self.FGEGA = "N 20th St, Morrow, GA 30260"
        self.FEGA = "100 Chamberlain Ave, Fort Eisenhower, GA 30905"
        self.FSGA = "266 W General Screven Way, Fort Stewart, GA 31313"
        self.FMGA = "Pearman St, Fort Moore, GA 31905"
        self.api_key = helper.get_key("maps")

    
    def _open_hor_csv(self) -> pd.DataFrame:
        """Private function open HORs.csv and return a pandas dataframe
        
        Args: None
        
        Returns: Pandas Dataframe."""
        
        df = pd.read_csv(self.hor_csv_path)
        return df
    
    def get_miles(self, meters: float) -> float:
        """Function that takes meters and converts them to miles
        
        Args: Float of meters to be converted
        
        Returns: Float of miles"""

        return meters*0.000621371192

    def _create_single_address(self) -> pd.DataFrame:
        """Private function that relies internally upon _open_hor_csv to concatenate the Home Address, 
        Home City, Home State and Home ZIP Code columns to feed into google maps
        
        Args: None
        
        Returns: Pandas Dataframe with new column: FullAddress"""

        df = self._open_hor_csv()
        full_address = []
        for homeaddress in zip(df['Home Address'], df['Home City'], df['Home State'], df['Home ZIP Code']):
            address, city, state, zipcode = homeaddress
            full_address.append(f"{address}, {city}, {state}, {zipcode}")
        
        df["FullAddress"] = full_address

        return df
    
    def _add_post_addresses(self) -> pd.DataFrame:
        """Private function that relies internally upon _create_single_address to create columns with
          addresses to the self.addresses in the __init__ function
    
        Args: None
        
        Returns: Pandas Dataframe with four new columns: FGEGA_Address, FEGA_Address, 
        FMGA_Address, FSGA_Address"""
        
        df = self._create_single_address()
        df["FGEGA_Address"]  = [self.FGEGA for address in range(len(df))]
        df["FEGA_Address"] = [self.FEGA for address in range(len(df))]
        df["FSGA_Address"]= [self.FSGA for address in range(len(df))]
        df["FMGA_Address"] = [self.FMGA for address in range(len(df))]

        return df
    
    def _remove_address(self, df: pd.DataFrame) -> pd.DataFrame:
        """Private function that will remove address columns and just leave the distances to each post
        per soldier to protect PII
        
        Args: df = pandas dataframe from self.get_time_and_distance
        
        Returns: pandas dataframe minus FullAddress, HomeAddress, HomeCity, HomeState, and HomeZipCode"""

        return df.drop(columns=["FullAddress", "Home Address", "Home City", "Home State", "Home ZIP Code", "FGEGA_Address", "FEGA_Address", "FSGA_Address", "FMGA_Address"])

    def get_time_and_distance(self) -> pd.DataFrame:
        """Meatiest function of entire class. Relies upon self._add_post_addresses to get final form of 
        dataframe. Then uses self.api_key to fetch the googlemaps API key.
        
        Args: None
        
        Returns: Pandas Dataframe with distances and times to each destination per soldier"""

        df = self._add_post_addresses()
        gmaps = gm.Client(self.api_key)
        

        FGEGA_Distance_Column = []
        FGEGA_Time_Column = []
        FEGA_Distance_Column = []
        FEGA_Time_Column = []
        FSGA_Distance_Column = []
        FSGA_Time_Column = []
        FMGA_Distance_Column = []
        FMGA_Time_Column = []
        home_county = []
        for index, row in df.iterrows():
            source_address = row["FullAddress"]

            address_info = gmaps.geocode(source_address)[0]
            county_json = [addr_com for addr_com in address_info.get("address_components") if "administrative_area_level_2" in addr_com["types"]]
            county_name = county_json[0].get("long_name").split(" ")[0]
            home_county.append(county_name)

            FGEGA_raw_data = gmaps.distance_matrix(source_address, row["FGEGA_Address"])['rows'][0]['elements'][0]
            FGEGA_Distance_Column.append("{:.2f}".format(self.get_miles(FGEGA_raw_data['distance']['value'])))
            FGEGA_Time_Column.append((str(timedelta(seconds=FGEGA_raw_data['duration']['value']))))

            FEGA_raw_data = gmaps.distance_matrix(source_address, row["FEGA_Address"])['rows'][0]['elements'][0]
            FEGA_Distance_Column.append("{:.2f}".format(self.get_miles(FEGA_raw_data['distance']['value'])))
            FEGA_Time_Column.append((str(timedelta(seconds=FEGA_raw_data['duration']['value']))))

            FSGA_raw_data = gmaps.distance_matrix(source_address, row["FSGA_Address"])['rows'][0]['elements'][0]
            FSGA_Distance_Column.append("{:.2f}".format(self.get_miles(FSGA_raw_data['distance']['value'])))
            FSGA_Time_Column.append((str(timedelta(seconds=FSGA_raw_data['duration']['value']))))

            FMGA_raw_data = gmaps.distance_matrix(source_address, row["FMGA_Address"])['rows'][0]['elements'][0]
            FMGA_Distance_Column.append("{:.2f}".format(self.get_miles(FMGA_raw_data['distance']['value'])))
            FMGA_Time_Column.append((str(timedelta(seconds=FMGA_raw_data['duration']['value']))))
        
        df['Home_County'] = home_county
        df['FGEGA_Distance'] = FGEGA_Distance_Column
        df['FGEGA_Time'] = FGEGA_Time_Column
        df['FEGA_Distance'] = FEGA_Distance_Column
        df['FEGA_Time'] = FEGA_Time_Column
        df['FSGA_Distance'] = FSGA_Distance_Column
        df['FSGA_Time'] = FSGA_Time_Column
        df['FMGA_Distance'] = FMGA_Distance_Column
        df['FMGA_Time'] = FMGA_Time_Column
        return self._remove_address(df)


