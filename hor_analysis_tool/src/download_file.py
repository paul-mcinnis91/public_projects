#!/usr/bin/env python3
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

from src import helper

class Download_Files:
    def __init__(self):
        """Constructor for Download Files. Creates self.downloads path and access to credentials relying
        upon the helper.py module"""

        credentials = helper.get_key("cloud")
        self.downloads_path = helper.get_downloads_directory()

        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = service_account.Credentials.from_service_account_file(
            credentials, scopes=self.SCOPES
        )
        self.service = build('drive', 'v3', credentials=self.creds)
    
    

    def list_files(self, page_size: int=10) -> list:
        """Lists files in Google Drive."""
        results = self.service.files().list(pageSize=page_size, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if not files:
            print("No files found.")
        else:
            for file in files:
                print(f"Found file: {file['name']} (ID: {file['id']})")
        return files
    
    def get_specific_file(self, file_name: str) -> dict:
        """Filters through list_files result to return the correct data
        
        Args: File Name
        
        Returns: Dictioanary"""

        file_list = self.list_files()
        correct_file_list = [file for file in file_list  if file["name"] == file_name]
        if len(correct_file_list) != 1:
            print(correct_file_list)
            exit()
        return correct_file_list[0]

    def download_file(self, file_id, file_name):
        """Downloads a file from Google Drive."""
        request = self.service.files().get_media(fileId=file_id)
        file_path = f'./{file_name}'  # Download location
        
        with io.FileIO(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")
        print(f"File downloaded successfully as {file_path}")

# Example usage:
if __name__ == "__main__":
    drive_downloader = Download_Files()
    
    # List files
    files = drive_downloader.get_specific_file("HORs.csv")
    print(files)
    
    # Example: Download first file in the list (if available)
    if files:
        file_id = files['id']
        file_name = files['name']
        drive_downloader.download_file(file_id, file_name)
