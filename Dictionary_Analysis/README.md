# Dictionary Etymology Puller

This Python script pulls etymology and origination dates for words using the Merriam-Webster Dictionary API.

## Features

- Fetches etymology and origination dates for words
- Handles API rate limiting (1000 calls per day)
- Saves progress to resume from where it left off
- Works on both Windows and Linux systems
- Saves results in a JSON file

## Prerequisites

- Python 3.x
- `requests` library

## Setup

1. Clone this repository
2. Install the required library:
   ```
   pip install requests
   ```
3. Create a `keys.txt` file in the same directory as the script with your Merriam-Webster API keys:
   ```
   YOUR_COLLEGIATE_API_KEY
   YOUR_MEDICAL_API_KEY
   ```
4. Ensure you have a `words_alpha.txt` file containing the list of words to process

## Usage

Run the script:

The script will:
1. Load the word list
2. Start processing words from where it last left off
3. Fetch etymology and origination date for each word
4. Save results to `etymology_dict.json`
5. Stop when it reaches 1000 API calls for the day

## Output

The script generates an `etymology_dict.json` file with the following structure for each word:


Ctrl+K to generate a command
Write and create a README.md for my  dictionary_pull.py

Here's a README.md file for your dictionary_pull.py script:
README.md
python dictionary_pull.py
json
{
"Index": 0,
"Word": "example",
"Etymology": "Latin exemplum",
"Origination Date": "14th century",
"URL": "https://www.dictionaryapi.com/api/v3/references/collegiate/json/example?key=YOUR_API_KEY",
"Web Response": [...]
}


## Notes

- The script uses the Collegiate Dictionary API
- API calls are limited to 1000 per day
- Progress is saved automatically, allowing you to resume from where you left off
- Adjust file paths in the `windows_linux_path` method if needed

## License

[MIT License](https://opensource.org/licenses/MIT)
