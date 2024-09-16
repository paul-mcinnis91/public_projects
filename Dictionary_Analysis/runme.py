import subprocess
import getpass
import os

if __name__ == "__main__":
    user = getpass.getuser()

    if os.name == 'nt':
        subprocess.run(["python3", fr"C:\Users\{user}\Projects\Dictionary_Analysis\setup.py"])
        subprocess.run(["python3", fr"C:\Users\{user}\Projects\Dictionary_Analysis\dictionary_pull.py"])
        subprocess.run(["python3", fr"C:\Users\{user}\Projects\Dictionary_Analysis\sync_files.py"])

    else:
        subprocess.run(["python3", f"/home/{user}/public_projects/Dictionary_Analysis/setup.py"])
        subprocess.run(["python3", f"/home/{user}/public_projects/Dictionary_Analysis/dictionary_pull.py"])
        subprocess.run(["python3", f"/home/{user}/public_projects/Dictionary_Analysis/sync_files.py"])
