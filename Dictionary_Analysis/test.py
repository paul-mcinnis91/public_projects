import json
from datetime import date
with open("api_calls.json", "r") as file:
    data = json.load(file)[0]
    print(data)
    # date = data["date"]
    # api_calls = data["api_calls"]

new_data = {"date": date.today().strftime("%Y-%m-%d"), "api_calls": 0}
with open("api_calls.json", "w") as file:
    json.dump(new_data, file, indent=2)

