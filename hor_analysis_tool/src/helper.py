import json
import os


def get_current_dir() -> str:
    """Returns current directory file is running in.
    
    Args: None
    
    Returns: current directory file is being run in."""
    return os.path.dirname(os.path.abspath(__file__))

def get_key(key_type) -> str:
    """Function that reads from apis.json to pull proper key
    
    Args: Key type, maps or cloud
    
    Returns: Key to google cloud storage"""
    current_dir = get_current_dir()
    keys_path = os.path.abspath(os.path.join(current_dir, "..", "keys"))
    pat_path = os.path.abspath(os.path.join(keys_path, "pat.txt"))
    api_path = os.path.abspath(os.path.join(keys_path, "api.txt"))
    
    if key_type == "maps":
        with open(api_path, "r") as json_data:
            return json_data.read()
    
    with open(pat_path) as pat_data:
        return pat_data.read()


def get_downloads_directory() -> str:
    """Function to get the absolute current downloads directory
    
    Args: None
    
    Returns: Absolute Path to current machine downloads directory"""

    current_user = os.getlogin()
    downloads_path = os.path.join("C:\\", "Users",  current_user, "Downloads")
    return downloads_path

def get_source_documents_directory() -> str:
    """Function to get the absolute source_documents directory
    
    Args: None
    
    Returns: absolute source_documents directory"""
    current_dir = get_current_dir()
    return os.path.abspath(os.path.join(current_dir, "..", "source_documents"))