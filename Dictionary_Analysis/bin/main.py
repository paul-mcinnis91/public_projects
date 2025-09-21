import json
from json import JSONDecodeError
import os
import sys

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.dictionary_pull import dictionary_pull

def main():
    """Main
    This function is the main function that runs the program.

    Args:
        None

    Returns:
        None
    """
    test_dictionary = dictionary_pull()
    current_index = test_dictionary.current_index()
    sorted_word_list = sorted(test_dictionary.word_list(), key=lambda x: x[0].lower())
    current_word_list = sorted_word_list[current_index:]
    if test_dictionary.last_date != test_dictionary.today_date:
        test_dictionary.current_api_calls = 0
    else:
        test_dictionary.current_api_calls = test_dictionary.current_api_calls()[0].get("api_calls")

    file_path = test_dictionary.windows_linux_path().get('etymology_dict')

    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except JSONDecodeError:
            data = []

        for idx, word in enumerate(current_word_list, start= current_index):

            print(f"Current API Calls: {test_dictionary.call_count}")

            if test_dictionary.call_count >= 1000:
                break
            etymology_row = {}

            word_json, url = test_dictionary.pull_dictionary(word)
            etymology = test_dictionary.etymology(word_json)
            word_date = test_dictionary.word_date(word_json)

            etymology_row["Index"] = idx
            etymology_row["Word"] = word
            etymology_row["Etymology"] = etymology
            etymology_row["Origination Date"] = word_date

            if etymology == "Unknown" and word_date == "Unknown":
                etymology_row["URL"] = url
                etymology_row["Web Response"] = word_json

            data.append(etymology_row)

        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()



if __name__ == "__main__":
    main()