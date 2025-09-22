import os
import sys

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push

def main():
    """Main
    This function is the main function that runs the program.

    Args:
        None

    Returns:
        None
    """
    dictionary_obj = dictionary_pull()
    current_index =  ld_pull.get_current_index()
    all_words_list = ld_pull.get_full_word_list()[current_index+1:]
    current_record_words = ld_pull.get_current_words()
    

    
    for idx, word in enumerate(all_words_list, start=current_index):
        word_json = dictionary_obj.pull_dictionary(word)
        if dictionary_obj.determine_known_unk(word_json):
            try:
                len_filtered = dictionary_obj.filter_for_len(word_json)
                full_package = dictionary_obj.package_et_date(json_response=len_filtered, index=idx, word=word)
                current_record_words.append(full_package)

            except AttributeError or IndexError:
                print(word_json)
                len_filtered = dictionary_obj.filter_for_len(word_json)
                full_package = dictionary_obj.package_et_date(json_response=len_filtered, index=idx, word=word)
                break
        
        if idx == current_index + 1000:
            print("Current Call Count: 1000")
            break
           
    
    ld_push.save_etymology_dict(current_record_words)


if __name__ == "__main__":
    main()