import sys
import os

import pandas as pd

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.local_terminal import Main_Menu



def main() -> None:
    """Main function to run Car Parts Web Crawler Module"""
    main_menu_obj = Main_Menu()
    main_menu_obj.run()
    

if __name__ == "__main__":

    main()