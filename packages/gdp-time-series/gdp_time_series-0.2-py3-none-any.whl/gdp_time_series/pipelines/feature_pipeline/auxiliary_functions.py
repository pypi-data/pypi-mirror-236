import re
import unicodedata
import pandas as pd


def has_diacritics_or_punctuation(input_string):
  # Use regex to find diacritics or punctuated letters
  pattern = r'[^\w\s]'
  pattern_match = re.search(pattern, unicodedata.normalize('NFKD', input_string))
  return bool(pattern_match)

# Constants for regex patterns and characters
COMMA_PATTERN = r'^(.*?),\s*(.*?)$'
DIACRITICS_PUNCTUATION_PATTERN = r'[^\w\s]'
SPACE_PATTERN = r'[^a-zA-Z0-9]+'
UNDERSCORE = '_'
SPACE = ' '

def preprocess_string(string):
    # Check for comma and process accordingly
    if ',' in string:
        rearranged_string = re.sub(COMMA_PATTERN, r'\2 \1', string).lower().replace(SPACE, UNDERSCORE).rstrip()
        if has_diacritics_or_punctuation(rearranged_string):
            rearranged_string = re.sub(DIACRITICS_PUNCTUATION_PATTERN, '', unicodedata.normalize('NFKD', rearranged_string)).lower().replace(SPACE, UNDERSCORE).rstrip(UNDERSCORE)
    # Check for diacritics or punctuation and process accordingly
    elif has_diacritics_or_punctuation(string):
        if '-' in string:
            rearranged_string = re.sub(r'[-]', UNDERSCORE, unicodedata.normalize('NFKD', string)).lower().replace(SPACE, UNDERSCORE).rstrip(UNDERSCORE)
            if has_diacritics_or_punctuation(rearranged_string):
                rearranged_string = re.sub(DIACRITICS_PUNCTUATION_PATTERN, '', unicodedata.normalize('NFKD', rearranged_string)).lower().replace(SPACE, UNDERSCORE).rstrip(UNDERSCORE)
        else:
            rearranged_string = re.sub(DIACRITICS_PUNCTUATION_PATTERN, '', unicodedata.normalize('NFKD', string)).lower().replace(SPACE, UNDERSCORE).rstrip(UNDERSCORE)
    # Process as a regular column name
    else:
        transformed_string = re.sub(SPACE_PATTERN, UNDERSCORE, string).lower()
        rearranged_string = transformed_string.rstrip(UNDERSCORE)

    return unicodedata.normalize('NFKD', rearranged_string).encode('ASCII', 'ignore').decode('utf-8')


# Function to process JSON data with preprocess_string
def process_dict_with_preprocess(data):
    for key, value in data.items():
        if isinstance(value, str):
            # If the value is a string, preprocess it using preprocess_string
            data[key] = preprocess_string(value)
        elif isinstance(value, dict):
            # If the value is a dictionary, recursively process it
            process_dict_with_preprocess(value)
        elif isinstance(value, list):
            # If the value is a list, recursively process each element
            for i, item in enumerate(value):
                if isinstance(item, str):
                    value[i] = preprocess_string(item)
                if isinstance(item, list):
                  for j,list_item in enumerate(item):
                    item[j] = preprocess_string(list_item)




