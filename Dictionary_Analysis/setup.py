import subprocess
import os

# Read the text document to get the repository URL and directory
with open('config.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        if key == "REPO_URL":
            repo_url = r"https://github.com/dwyl/english-words.git"
        elif key == "CLONE_DIR":
            if os.name == "nt":
                  clone_dir = f"{os.path.expanduser('~')}\english-words"
            else:
                clone_dir = f"{os.path.expanduser('~')}/english-words"

# Clone the repository using git
subprocess.run(["git", "clone", repo_url, clone_dir])