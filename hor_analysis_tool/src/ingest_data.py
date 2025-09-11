#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import helper

class Ingest_Data:

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.downloads_path = helper.get_downloads_directory()

    def check_downloads(self) -> list:
        """"Check downloads function. Makes sure there is only one download and returns a list with that one file path
        If there is more than one file path: If it does not, it clears downloads, emails the origin email
        and exits the program.

        Args: None
        
        Returns: List with one file path"""
        
        directory = Path(self.downloads_path)
        file_paths = [str(file) for file in directory.iterdir() if file.is_file()]
        if len(file_paths) != 1:
            self.clear_downloads()
            self.email_failed_script()
            exit(1)
        return file_paths

    def pull_csv_download(self) -> str:
        """Pull CSV Download function. Relies upon self.check_downloads to get list with one item.
        Pulls single item, checks if ends with '.csv'. If it does not, it clears downloads, emails the origin email
        and exits the program.
        
        Args: None
        
        Returns: csv path string"""

        file_paths: list = self.check_downloads()
        csv_path: str = file_paths[0]
        if csv_path.endswith(".csv"):
            return csv_path
        self.clear_downloads()
        self.email_failed_script()
        exit(1)

    def template_column_list(self) -> list:
        """Pulls list of column names from source_documents/HOR_Template.csv
        
        Args: None
        
        Returns: list of correct columns"""

        hor_template_path = os.path.join(helper.get_source_documents_directory(), "hor_template.csv")
        hor_template = pd.read_csv(hor_template_path)
        return hor_template.columns.to_list()



    def eliminate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function to remove unneeded columns to fit criteria for columns. 
        Hopefully makes things a little bit simpler
        
        Args: df a pandas dataframe that is fed into the the function
        
        Returns: df with less columns to pass column test"""

        # Fetch the names for the template
        template_column_names = self.template_column_list()

        # Iterate through them and drop all unneeded ones
        for column in df.columns:
            if column not in template_column_names:
                df = df.drop(axis=1, columns=column)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(current_dir, "..", "source_documents", f"HORs.csv"))
        df.to_csv(csv_path, index=False)
        return df


    def test_file_columns(self, csv_columns: list, from_email: bool = False) -> None:
        """Checks the file columns of the given list against a list pulled from the hor_template.csv
        If there is no match, clears the downloads, emails a failure script, then
        raises a value error and exits the program
        
        Args: csv_columns a list of the csv columns to be tested against the template
        
        Returns: Value Error if columns do not match the template"""

        template_column_names = self.template_column_list()

        if sorted(template_column_names) != sorted(csv_columns):
            # Test if the file originated from an email
            if from_email:
                self.clear_downloads()
                self.email_failed_script()
            raise ValueError(f"Incorrect Column names expected {template_column_names} and got {csv_columns}")


    def get_file_columns(self, hor_csv_path: Path = None) -> str:
        """Check file columns function. Relies upon hor_template.csv to check if columns in file match columns in delivered file. 
        If it does not, it clears downloads, emails the origin email and exits the program.
        
        Args: None
        
        Returns: path to current hor csv"""
        

        if hor_csv_path == None:
            current_hor_csv_path = self.pull_csv_download()
            current_hor_csv = pd.read_csv(current_hor_csv_path)
            reduced_columns_csv = self.eliminate_columns(current_hor_csv)
            current_hor_columns = reduced_columns_csv.columns.to_list()
            self.test_file_columns(from_email=True)
        else:
            current_hor_csv_path = hor_csv_path
            current_hor_csv = pd.read_csv(hor_csv_path)
            reduced_columns_csv = self.eliminate_columns(current_hor_csv)
            current_hor_columns = reduced_columns_csv.columns.to_list()
            self.test_file_columns(csv_columns=current_hor_columns)


        return current_hor_csv_path

    def clear_downloads(self):
        """Goes to download directory and deletes all files when called
        
        Args: None
        
        Returns: None"""

        download_directory = Path(self.downloads_path)
        for file_folder in download_directory.iterdir():
            os.remove(file_folder)

    def read_json_file(self, json_file_path: str) -> dict:
        """Function to read json file and return data as a dictionary. Used to reduce McCabe Score
        
        Args: json_file_path = string path leading to the json file
        
        Returns: Dictionary"""

        with open(json_file_path, 'r') as file_data:
            data = json.load(file_data)
            return data
        
    def email_failed_script(self):
        """Emails the email that sent the csv file and tells them it's not working.
        
        Args: None
        
        Returns: None"""
        current_dir = self.current_dir

        email_json_path = os.path.join(current_dir, "..", "keys", "email.json")

        email_information = self.read_json_file(email_json_path).get("email_info")
        sender_email = email_information["user"]

        email_password = email_information["password"]
        email_server = email_information["server"]

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = sender_email
        msg["Subject"] = f"{os.path.basename(__file__)} script failed."

        # Email body
        body = (
            f"Reasons {os.path.basename(__file__)} fails:\n"
            " 1) Downloads folder not clear\n"
            "\n"
            " 2) The columns in your csv file did match the HOR_Template.csv\n"
            "\n"
            " 3) The file type was not a .csv"
        )
        msg.attach(MIMEText(body, "plain"))
        
        # SMTP server setup and send email
        server = smtplib.SMTP(email_server, 587)  # Use Outlook's server if needed
        server.starttls()  # Secure the connection
        server.login(sender_email, email_password)
        server.send_message(msg)
        server.quit()

    

    def mov_file(self, hor_csv_path: Path = None) -> Path:
        """Renames designated file to HORs.csv then moves to source_documents
        
        Args: None
        
        Returns: final csv path since all checks have been completed."""
        final_csv_path = os.path.abspath(os.path.join(helper.get_source_documents_directory(), "HORs.csv"))

        if hor_csv_path == None:
            # If no argument passed then check file columns from downloads
            new_hor_csv_path = self.get_file_columns()
            shutil.move(new_hor_csv_path, final_csv_path)            
        
        else:
            # If an argument is passed then check file columns from passed file
            new_hor_csv_path = self.get_file_columns(hor_csv_path=hor_csv_path)
            shutil.move(new_hor_csv_path, final_csv_path)
        
        return final_csv_path

if __name__ == "__main__":
    test_obj = Ingest_Data()
    test_obj.clear_downloads()