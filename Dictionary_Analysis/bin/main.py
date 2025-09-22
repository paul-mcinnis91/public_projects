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
    all_words = ld_pull.get_full_word_list()
    current_record_words = ld_pull.get_current_words()

    for idx, word in enumerate(all_words, start=current_index):
        word_json = test_dictionary.pull_dictionary(word)
        len_filtered = test_dictionary.filter_for_len(word_json)
        full_package = test_dictionary.package_et_date(json_response=len_filtered, index=idx, word=word)



    


    
    
    



    
        



if __name__ == "__main__":
    main()