import re

character_string = "Unknown"

x = re.sub(r'[^a-zA-Z0-9\s]', '', character_string)
print(x)