import re

def check_bank(text):
    # Define the regular expression pattern to match any of the specified bank names
    pattern = r'\b(morgan stanley|barclays|ubs|deutsche bank|j\.?p\.?\s?morgan|jpmorgan|goldman sachs|gs|bank of america|boa|bofa|citi|citigroup|bank of shanghai|shanghai pudong development bank|raymond james|oppenheimer|keybank|stifel|wells fargo|piper sandler|william blair|scotiabank)\b'



    # Search for the p  attern in the text, ignoring case
    return bool(re.search(pattern, text, re.IGNORECASE))

# Example usage
# print(check_bank("This is a test string with Morgan Stanley in it."))  # Output: True
# print(check_bank("Checking account with UBS and other details."))     # Output: True
# print(check_bank("This string does not contain any bank names."))      # Output: False
# print(check_bank("Deutsche bank is mentioned here."))                 # Output: True
# print(check_bank("Barclays is a well-known bank."))                   # Output: True
