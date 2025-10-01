from datetime import date
import os
import sys
import subprocess
import time

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull
from src import local_data_pull as ld_pull
from src import local_data_push as ld_push
from src.data_cleanse import Data_Cleanse
from src.data_vis import Data_Visualizations

def main(visualization_choice: str):
    """Main
    This function is the main function that runs the program.

    Args:
        None

    Returns:
        None
    """
    dictionary_obj = dictionary_pull()
    current_index =  ld_pull.get_current_index()
    all_words_list = ld_pull.get_word_lang_list("words_alpha")
    current_words = all_words_list[:current_index]
    current_idx_all_words_list = all_words_list[current_index+1:]
    current_record_words = ld_pull.get_current_words()
    data_cleaner = Data_Cleanse()
    data_vis = Data_Visualizations()

    
    for idx, word in enumerate(current_idx_all_words_list, start=current_index):
        
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
    
    ld_push.save_etymology_dict(current_record_words)

    cleaned_words = data_cleaner.cleaned_list(current_record_words)
    dirty_words = data_cleaner.dirty_list(current_words, cleaned_words)


    ld_push.save_clean_et_dict(cleaned_words)
    ld_push.save_dirty_list(dirty_words)

    subprocess.run(["dir"], shell = True)
    subprocess.run(["cd", ".."], shell = True)
    subprocess.run(["git", "add", "."], shell = True)
    subprocess.run(["git", "commit", "-m", f"Daily run for date: {date.today()}"], shell = True)
    subprocess.run(["git", "push"], shell = True)

    if not isinstance(visualization_choice, type(None)):
        data_vis.visualiziations(visualization_choice)
    
    time.sleep(60)
    
    data_vis.exit_gracefully()


if __name__ == "__main__":
    try:
        visualization_dec = sys.argv[1]
        main(visualization_dec)
    except IndexError:
        main(None)
