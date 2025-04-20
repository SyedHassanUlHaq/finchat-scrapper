import re

def check_bank(text):
    # Define the regular expression pattern to match any of the specified bank names
    pattern = r'\b(morgan stanley|barclays|ubs|deutsche bank|j\.?p\.?\s?morgan|jpmorgan|goldman sachs|gs|bank of america|boa|bofa|citi|citigroup|bank of shanghai|shanghai pudong development bank|raymond james|oppenheimer|keybank|stifel|wells fargo|piper sandler)\b'



    # Search for the p  attern in the text, ignoring case
    return bool(re.search(pattern, text, re.IGNORECASE))

# Example usage
# print(contains_us_bank_name("This is a test string with Morgan Stanley in it."))  # Output: True
# print(contains_us_bank_name("Checking account with UBS and other details."))     # Output: True
# print(contains_us_bank_name("This string does not contain any bank names."))      # Output: False
# print(contains_us_bank_name("Deutsche bank is mentioned here."))                 # Output: True
# print(contains_us_bank_name("Barclays is a well-known bank."))                   # Output: True
