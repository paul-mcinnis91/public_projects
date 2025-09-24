import os
import sys

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push
from src.data_cleanse import Data_Cleanse

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
    all_words_list = ld_pull.get_word_lang_list("words_alpha")[current_index+1:]
    current_record_words = ld_pull.get_current_words()
    data_cleaner = Data_Cleanse()
    

    
    for idx, word in enumerate(all_words_list, start=current_index):
        
        if dictionary_obj.call_count >= 1000:
            print(f"Current Call Count: {dictionary_obj.call_count}. Max usage is 1000 calls a day")
            break
           
        word_json = dictionary_obj.pull_dictionary(word)
        if dictionary_obj.determine_known_unk(word_json):
            try:
                len_filtered = dictionary_obj.filter_for_len(word_json)
                full_package = dictionary_obj.package_et_date(json_response=len_filtered, index=idx, word=word)
                current_record_words.append(full_package)

            except TypeError:
                print(word_json)
                len_filtered = dictionary_obj.filter_for_len(word_json)
                full_package = dictionary_obj.package_et_date(json_response=len_filtered, index=idx, word=word)
                break
    
    cleaned_words = data_cleaner.cleaned_list(current_record_words)
    
    ld_push.save_etymology_dict(cleaned_words)


if __name__ == "__main__":
    main()