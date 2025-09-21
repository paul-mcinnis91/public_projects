import os
import sys

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull
from src import local_data_pull as ldp

def main():
    """Main
    This function is the main function that runs the program.

    Args:
        None

    Returns:
        None
    """
    test_dictionary = dictionary_pull()
    current_index =  ldp.get_current_index()
    sorted_word_list = ldp.get_full_word_list()
    current_word_list = sorted_word_list[current_index:]
    
    current_word_list: list = ldp.get_current_words()

    print(current_word_list[-1]) 

    
        



if __name__ == "__main__":
    main()