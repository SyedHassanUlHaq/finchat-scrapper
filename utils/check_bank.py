import re

def check_bank(text):
    # Define the regular expression pattern to match any of the specified bank names
    pattern = r'\b(morgan stanley|barclays|ubs|deutsche|j\.?p\.?\s?morgan|jpmorgan|goldman sachs|goldman\s?sachs|gs)\b'

    # Search for the pattern in the text, ignoring case
    return bool(re.search(pattern, text, re.IGNORECASE))

# Example usage
# print(contains_us_bank_name("This is a test string with Morgan Stanley in it."))  # Output: True
# print(contains_us_bank_name("Checking account with UBS and other details."))     # Output: True
# print(contains_us_bank_name("This string does not contain any bank names."))      # Output: False
# print(contains_us_bank_name("Deutsche bank is mentioned here."))                 # Output: True
# print(contains_us_bank_name("Barclays is a well-known bank."))                   # Output: True
