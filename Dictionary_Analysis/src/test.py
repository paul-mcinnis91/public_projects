import re

x = 'before 12th century{ds||1||}'
cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', x)
print(cleaned)