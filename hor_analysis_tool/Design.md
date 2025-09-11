# hor_scripts
hor_scripts is a python module broken into several different folders.
bin holds main.py
keys holds the api keys and example api keys
requirements holds requirements.txt for the pip freeze
source_documents holds HOR_template as an example
src holds driving_distance.py which is the meat and potatoes of the module

# bin

## main.py
main.py appends the sys.path variable to include the parent directory hor_scripts which allows import of src/driving_distance.py.Driving_Distance

If main is being ran as the main file and not imported the code will execute. Otherwise nothing will happen besides the sys.path variable being updated.

# src
Main calls upon files in the following order:
1. ingest_data.py
2. driving_distance.py
3. git_push.py
4. email.py

## ingest_data.py
File that will be triggered by windows task scheduler. The task scheduler will run the script once an hour or once a day to ensure timely turn around of data.

### Ingest_Data Class

#### __init___
Takes 0 arguments. Creates a few attributes for use later in the program.
Attrs:
    current_dir: Current directory of the file at runtime
    current_user: Current user on the computer at runtime
    downloads_path: Downloads directory based upon current_dir and current_user

#### check_downloads
If length of the downloads is not 1, calls upon clear_downloads, then email_failed_script then exits the program.
If length of the downloads is 1, returns list with downloaded file path.

#### pull_csv_download
Pulls full file path of all items in downloads.
Calls check_downloads.
Checks if file path ends with .csv. If no, calls upon clear_downloads, then email_failed_script then exits the program
Returns csv file_path if check_downloads is successful.


#### check_file_columns
Relies upon pull_csv_download
Opens csv with pandas and checks that columns meet the column names.
If criteria is met, returns file path. 
If criteria is not met, calls email_failed_script, then exits program.

#### clear_downloads
Moves all items in downloads to recycling bin.

#### email_failed_script
Sends email back to calling upon __file__ to send file name stating it failed.

#### mov_file
Calls upon check_file_columns, if successful: moves file to source_documents using shutil.

## driving_distance.py
driving_distance.py is the meat and potatoes of the module / library. It contains the Driving_Distances class and a few private and public methods to return the driving times and distances. The other columns besides these need to be added. This script will remain as it is because it has singular focus.

### Driving_Distance Class

#### __init___
Takes one argument for the HORs.csv once it has been scrubbed by the Ingest_Data Class. 
FGEGA, self.FEGA, self.FSGA, self.FMGA attributes which are addresses to Fort Gillem Enclave GA, Fort Eisenhower GA, Fort Stewart GA, and Fort Moore GA.

Then creates self.api_key by calling up self._get_api_key() documented below.

#### _get_api_key
Takes no arguments. Gets parent directory and keys directory to pull data from keys.txt. Returns text within keys.txt

#### _open_hor_csv
Takes no arguments. Returns panda dataframe Gets path to source_documents get the HORs.csv path then creates a data frame by using pd.read_csv.

#### get_miles
Takes meters as a float argument. Returns meters in miles format.

#### _create_single_address
Takes no arguments. Returns panda dataframe.
Relies upon _open_hor_csv to get pandas dataframe. Concatenates Home Address, Home City, Home State and Home ZIP Code to create column FullAddress. 

#### _add_post_addresses
Takes no argument. Returns panda dataframe.
Relies upon _create_single_address to get pandas datframe. Uses self.FGEGA, self.FEGA, self.FSGA, and self.FMGA and list comprehension based upon the length of the dataframe from _create_single_address to create 4 new columns. These columns are the addresses to the 4 aforementiond posts discussed in the __init__ function.

#### _remove_address
Takes pandas dataframe as an argument. Returns pandas dataframe. Drops FullAddress, Home Address, Home State, Home ZIP Code, FGEGA_Address, FEGA_Address, FSGA_Address, and FMGA_Address so that the soldiers PII is protected and we can reduce unneeded columns

#### get_time_and_distance
Takes no argument, returns pandas dataframe.
Meat of the class and brings all prior steps together to get actual data we need. 
Gets initial dataframe from _add_post_addresses
Creats googlemaps.Client class from googlemaps.Client. Client class needs an api key which it receives from self.api_key.
After client object and dataframe are instantiated then 8 lists are created. Two for each military post. One is the distance, one is the time. The lists are empty at first.
Using the iterrows method raw data is gathered and then distance and time are extracted by calling the get_miles function.
Once the iteration is complete the dataframe is modified by adding the 8 new columns which match the 8 now full list names.
The dataframe is return after being run through the _remove_address method. 

## git_push.py
Uses functional programming as opposed to OOP because there should be minimal errors at this stage.

### get_personal_acc_tok
Gets personal access token if needed for revalidation

### git_push
Calls upon subprocess and datetime to run three commands: 
    git add .
    git commit -m "Adding HORs for {date}"
    git push
    exit()

## email.py


