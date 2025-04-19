import re

def extract_quarter_and_year(text):
    # Define the regular expression pattern to match the quarter and year
    pattern = r'\bQ(\d)\s+(\d{4})\b'
    # Search for the pattern in the text
    match = re.search(pattern, text)
    if match:
        quarter = match.group(1)
        year = match.group(2)
        return int(quarter), int(year)
    return None, None

# Example usage
quarter, year = extract_quarter_and_year("Q3 2021 - October 26, 2021")
print(f"Quarter: {quarter}, Year: {year}")  # Output: Quarter: 3, Year: 2024
