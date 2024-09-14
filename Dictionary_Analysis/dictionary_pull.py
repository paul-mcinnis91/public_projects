import requests
import json
import os
import atexit
from json import JSONDecodeError
from datetime import date

class dictionary_pull:
    """Dictionary Pull Class
    This class is used to pull the etymology of words from the dictionaryapi.com API.
    It is used to create a dictionary of words and their etymologies.

    The Constructor builds the API keys and sets the current API calls to the value in the json file.
    It also sets the today's date and registers the save_api_calls function to be called when the program is closed.

    At Exit, it saves the API calls to the json file.

    Args:
        None

    Returns:
        None
    """
    def __init__(self):
        college_key, self.medical_key = self.dictionary_keys()
        self.college_key = college_key.strip()
        self.today_date = date.today().strftime("%Y-%m-%d")
        self.call_count = self.current_api_calls()[0]["api_calls"]
        self.last_date = self.current_api_calls()[0]["date"]
        atexit.register(self.save_api_calls)

    def windows_linux_path(self):
        file_path_dict = {}
        if os.name == "nt":
            file_path_dict["api_calls"] = r"C:\Users\Michel´s PC\Projects\Dictionary_Analysis\api_calls.json"
            file_path_dict["words_alpha"] = r"C:\Users\Michel´s PC\english-words\words_alpha.txt"
            file_path_dict["etymology_dict"] = r"C:\Users\Michel´s PC\Projects\Dictionary_Analysis\etymology_dict.json"
            file_path_dict["keys"] = r"C:\Users\Michel´s PC\Projects\Dictionary_Analysis\keys.txt"
            return file_path_dict

        else:
            try:
                open(r'/home/william.p.mcinnis53/Projects/Dictionary_Analysis/keys.txt')
                file_path_dict["api_calls"] = r"/home/william.p.mcinnis53/Projects/Dictionary_Analysis/api_calls.json"
                file_path_dict["words_alpha"] = r"/home/william.p.mcinnis53/english-words/words_alpha.txt"
                file_path_dict["etymology_dict"] = r"/home/william.p.mcinnis53/Projects/Dictionary_Analysis/etymology_dict.json"
                file_path_dict["keys"] = r"/home/william.p.mcinnis53/Projects/Dictionary_Analysis/keys.txt"
                return file_path_dict
            except FileNotFoundError:
                file_path_dict["api_calls"] = r"/home/paulmcinnis/Projects/Dictionary_Analysis/api_calls.json"
                file_path_dict["words_alpha"] = r"/home/paulmcinnis/english-words/words_alpha.txt"
                file_path_dict["etymology_dict"] = r"/home/paulmcinnis/Projects/Dictionary_Analysis/etymology_dict.json"
                file_path_dict["keys"] = r"/home/paulmcinnis/Projects/Dictionary_Analysis/keys.txt"
                return file_path_dict

    def save_api_calls(self):
        """Save API Calls
        This function saves the API calls to the json file.

        Args:
            None

        Returns:
            None
        """
        file_path = self.windows_linux_path()['api_calls']

        with open(file_path, "w") as file:
            try:
                data = [{"api_calls": self.call_count, "date": self.today_date}]
                json.dump(data, file, indent=2)
            except TypeError:
                data = [{"api_calls": 0, "date": {self.today_date}}]
                json.dump(data, file, indent=2)

    def current_api_calls(self):
        """Current API Calls
        This function returns the current API calls from the json file and the last date the API calls were updated.

        Args:
            None

        Returns:
            None
        """
        file_path = self.windows_linux_path()['api_calls']
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if data[0]["date"] != self.today_date:
                    data[0]["api_calls"] = 0
                return data
        except JSONDecodeError:
            return {"api_calls": 0, "date": self.today_date}

    def word_list(self) -> set:
        """Word List
        This function returns a set of words from the words_alpha.txt file.

        Args:
            None

        Returns:
            None
        """
        file_path = self.windows_linux_path()['words_alpha']
        with open(file_path, "r") as file:
            return(sorted(set(file.read().split()), key=lambda x: x.lower()))

    def pull_dictionary(self, word) -> list:
        """Pull Dictionary
        This function pulls the dictionary from the dictionaryapi.com API.

        Args:
            word (str): The word to pull the dictionary for.

        Returns:
            None
        """
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.college_key}"
        response = requests.get(url)
        self.call_count += 1
        return response.json(), url

    def etymology(self, json_response: list) -> str:
        """Etymology
        This function returns the etymology of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            None
        """
        try:
            json_response[0].keys()
        except AttributeError:
            return "Unknown"

        try:
            return json_response[0]["et"][0]
        except KeyError:
            return "Unknown"

    def word_date(self, json_response: list) -> str:
        """Word Date
        This function returns the origination date of a word from the json response.

        Args:
            json_response (list): The json response from the dictionaryapi.com API.

        Returns:
            None
        """
        try:
            json_response[0].keys()
        except AttributeError:
            return "Unknown"
        try:
            origination_date = json_response[0]["date"]
            if origination_date.isdigit():
                return int(origination_date)
            else:
                return origination_date
        except KeyError:
            return "Unknown"

    def dictionary_keys(self) -> list:
        """Dictionary Keys
        This function returns the API keys from the keys.txt file.

        Args:
            None

        Returns:
            None
        """
        file_path = self.windows_linux_path()["keys"]
        with open(file_path, "r") as f:
            return f.readlines()

    def current_index(self) -> int:
        """Current Index
        This function returns the current index of the word list from the etymology_dict.json file.

        Args:
            None

        Returns:
            None
        """
        file_path = self.windows_linux_path()["etymology_dict"]
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                return len(data)
        except FileNotFoundError:
            return 0

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
        test_dictionary.current_api_calls = test_dictionary.current_api_calls()[0]["api_calls"]

    file_path = test_dictionary.windows_linux_path()['etymology_dict']

    with open(file_path, "r+") as f:
        try:
            data = json.load(f)
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

        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()



if __name__ == "__main__":
    main()