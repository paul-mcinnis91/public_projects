import os
import sys

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull
from src import local_data_pull as ld_pull

def main():
    """Main
    This function is the main function that runs the program.

    Args:
        None

    Returns:
        None
    """
    test_dictionary = dictionary_pull()
    current_index =  ld_pull.get_current_index()
    sorted_word_list = ld_pull.get_full_word_list()
    current_word_list = sorted_word_list[current_index:]
    
    current_word_list: list = ld_pull.get_current_words()
    all_word_list: list = ld_pull.get_full_word_list()

    print(current_word_list[-1]) 
    print(all_word_list[current_index-1])


    
        



if __name__ == "__main__":
    main()