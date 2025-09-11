# hor_scripts

# Overview:
This python program uses by python 3.8.10
This python program relies upon paid access to googlemaps API key.
The python program will use Pandas, and googlemaps python modules to function. 
The format for the csv document will be as follows:
SoldierName, Title, Home Address, Home City, Home State, Home ZIP Code
The column Title is the Soldiers DOD ID. The column is named Title because in Sharepoint their must be a "Title" Column. And since this column is always there we made the Title column our key / foreign key column.
All columns with the exception of SoldierName and Title will be concatenated together before being ran through the script to get an accurate Home of Record (HOR) to feed to the google maps API. 

# Purpose:
This program will be ran once a month on a timer to check if soldiers in the 111th EW company will need hotels for home station training (HOST), or if they will be a direct report to any of the posts in Georgia. 
The posts we will check against are:
Fort Gillem, GA (HOST): N 20th St, Morrow, GA 30260 
Fort Moore / Benning, GA: Pearman St, Fort Moore, GA 31905
Fort Eisenhower / Gordon, GA: 100 Chamberlain Ave, Fort Eisenhower, GA 30905
Fort Stewart, GA: 266 W General Screven Way, Fort Stewart, GA 31313

# Future Goal:
Find a way to have this done in power automate as power automate has a bings map connector and will output distances. It is currently forbidden under our plan right now despite being a free connector.

Barring that, store this program on a server at the armory, run once a month to validate soldier contact information.

# How to use: 

1) Follow the instructions in api_example.txt
2) Follow the instructions in pat_example.txt
3) Run pip install -r requirements.txt on the requirements.txt document located under requirements
4) Place the HORs.csv into the source_documents directory
5) Once api.txt is created with YOUR API KEY, and you have pip installed all the requirements in requirements.txt;
5a) run main.py from the /bin/ directory if you are using the email feature. This piece has bugs and is deprecated, as it violates PII regulations. 
5b) run main.py from the /bin/ directory with ../source_documents/HORs.csv as the only argument

Once the program finishes running it will deposit the latest version of the file into source_documents as YYYY-MM-DD_111_driving_distances.csv

6) Git push the entire module with the current file onto the remote repo
7) Download the latest driving distances csv onto Army AVD
8) Navigate to senior leaders private site contents found here (can only be accessed on AVD):

9) Open the 111_driving_distances sharepoint list
10) Select all entries, and delete them
11) Open the driving distances csv from your Army AVD Downloads directory
12) Select all items in the csv, copy them
13) Go back to the 111_driving_distances sharepoint list
14) Edit the 111_driving_distances sharepoint list in grid view
15) Paste the contents of the driving distances csv into the sharepoint list

You're done. The power BI dashboard will refresh at midnight. If it does not contact tech support (1SG McInnis, if he's no longer there good luck!)

Then in source_documents a new csv in the format today's_date_111_driving_distance.csv will be there. Take that csv and update the sharepoint list in the senior leaders private channel on sharepoint. 

Then you're done!

# Mermaid Flowchart

flowchart TD
%% Nodes
    A("1st of month or button hit")
    B("Power Automate sends email attachment")
    C("Outside email downloads email attachment")
    D("Python file monitoring downloads is triggered")
    E("hor.py is run")
    F("hor.py output is saved to directory")
    G("Python module to email back file is triggered")
    H("Power Automate is triggered to update Sharepoint List")

    

%% Edge connections between nodes
    A --> B -- Sent outside AVD / NIPR--> C --> D
    D --> E --> F --> G
    G -- Sent back into AVD / NIPR --> H

   



# mccabe score

## driving_distance.py:
8:4: 'Driving_Distance.__init__' 1
17:4: 'Driving_Distance._get_api_key' 1
29:4: 'Driving_Distance._open_hor_csv' 1
39:4: 'Driving_Distance.get_miles' 1
48:4: 'Driving_Distance._create_single_address' 2
66:4: 'Driving_Distance._add_post_addresses' 1
83:4: 'Driving_Distance._remove_address' 1
93:4: 'Driving_Distance.get_time_and_distance' 2

## ingest_data.py:
10:4: 'Ingest_Data.__init__' 1
15:4: 'Ingest_Data.check_downloads' 2
32:4: 'Ingest_Data.pull_csv_download' 2
50:4: 'Ingest_Data.check_file_columns' 2
74:4: 'Ingest_Data.clear_downloads' 2
85:4: 'Ingest_Data.email_failed_script' 1
94:4: 'Ingest_Data.mov_file' 1
