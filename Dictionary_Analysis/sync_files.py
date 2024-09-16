import json
import os
import getpass
import difflib

if __name__ == "__main__":
    user = getpass.getuser()

    if os.name == 'nt':
        public_json = fr"C:\Users\{user}\public_projects\Dictionary_Analysis\etymology_dict.json"
        private_json = fr"C:\Users\{user}\Projects\Dictionary_Analysis\etymology_dict.json"
    else:   
        public_json = f"/home/{user}/public_projects/Dictionary_Analysis/etymology_dict.json"
        private_json = f"/home/{user}/Projects/Dictionary_Analysis/etymology_dict.json"
        
    with open(public_json, 'r') as pub_json:
        public_data = json.load(pub_json)
    
    with open(private_json, 'r') as priv_json:
        private_data = json.load(priv_json)
    

    if len(public_data) > len(private_data):
        with open(private_json, 'w') as priv_json:
            json.dump(public_data, priv_json)
    
    elif len(private_data) > len(public_data):
        with open(public_json, 'w') as pub_json:
            json.dump(private_data, pub_json)

    else:
        print(f"Public JSON Length = {len(public_data)}")
        print(f"Private JSON Length = {len(private_data)}")
        print("Files are the same!")
        