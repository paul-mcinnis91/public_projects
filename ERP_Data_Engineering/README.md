# ERP_Data_Engineering

# Overview:
This python program uses python 3.8.10
This program relies heavily upon Selenium, and salesforce_reporting modules

# Purpose: 
This program will be ran twice a week on Monday and Thursday to download data from Oracle Business Intelligence (OBI). Once the files are downloaded from Oracle Business Intelligence into the downloads directory, they are moved from there into the appropriate directory for the ETL process to begin. The program can be run by using windows task scheduler and the python engine. For some reason the organization the author worked with at the time of creation of this program did not have back end access to their own data in OBI...

# Future Goal:
Clean this code to obfuscate all file paths and user credentials. When this was written in 2022 the author was unaware of these security issues and wrote programs as such.

# How to use: 

1) In the keys directory create a file called user.txt and add your username
2) In the keys directory create a file called pw.txt and add your password
3) Run the pyproject.toml to setup and run
4) Login to the VPN for this organization
5) Run main.py


# mccabe score

## check_downloads.py:
13:4: 'Check_Downloads.__init__' 1
17:4: 'Check_Downloads.check_files_downloaded' 3
56:4: 'Check_Downloads.download_missed_files' 4
84:4: 'Check_Downloads.login_download_check_redownload' 1

## helper.py:
6:0: 'day_of_week_fun' 2
15:0: 'manual_override' 2
24:0: 'day_of_week_check' 2
41:0: 'get_current_dir' 1
50:0: 'get_user_creds' 1
69:0: 'move_files' 1
75:0: 'attachment_rate_rename' 1
91:0: 'move_and_rename_files' 4

## OBI_Downloads.py:
19:4: 'DownloadFilesfromOBI.__init__' 1
23:4: 'DownloadFilesfromOBI.OBI_Login' 1
52:4: 'DownloadFilesfromOBI._catalog_loop_mon' 2
64:4: 'DownloadFilesfromOBI._catalog_loop_thurs' 4
93:4: 'DownloadFilesfromOBI.navigate_catalog' 2
121:4: 'DownloadFilesfromOBI.download_files_mon' 4
142:4: 'DownloadFilesfromOBI.failed_thurs_download' 3
157:4: 'DownloadFilesfromOBI.download_files_thurs' 5
177:4: 'DownloadFilesfromOBI.download_files' 2

## salesforce_data_pull.py
10:0: 'salesforce_UVO_pull' 1
52:0: 'record_data' 1
