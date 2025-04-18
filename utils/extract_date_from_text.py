import re
from datetime import datetime

from datetime import datetime
import re

from datetime import datetime
import re

def convert_and_extract_date(text):
    if text is None:
        return None
    # Normalize the text by removing extra spaces and converting to lower case
    normalized_text = re.sub(r'\s+', ' ', text).strip().lower()

    # Define the regular expression pattern for the given date format
    pattern = (
        r'\b(?:january|february|march|april|may|june|july|august|'
        r'september|october|november|december)\s*\d{1,2},\s*\d{4}\b'
    )

    # Search for the pattern in the normalized text
    match = re.search(pattern, normalized_text)
    if match:
        # Convert the matched date to datetime object
        date_str = re.sub(r'\s+', '', match.group(0))  # Remove spaces for parsing
        date_obj = datetime.strptime(date_str, '%B%d,%Y')
        # Return the date in yyyy-mm-dd format
        return date_obj.strftime('%Y-%m-%d')
    return None

# Test the function with various cases
# test_cases = [
#     "Q2 2024 - July 23, 2024",
#     "Q2 2024 - july23,2024",
#     "Q2 2024 -   July   23  ,  2024  ",
#     "q2 2024 - JULY 23, 2024"
# ]

# extracted_dates = [convert_and_extract_date(tc) for tc in test_cases]
# print(extracted_dates)


def extract_date_from_text(text):
    """
    Extract the first date from text in various formats (case-insensitive).
    Returns the date in 'yyyy-mm-dd' format or None if no date is found.
    
    Handles formats like:
    - Q1 2025 → returns first day of quarter (2025-01-01)
    - January 30, 2025 → 2025-01-30
    - 30-Jan-2025 → 2025-01-30
    - 2025-01-30 → 2025-01-30
    - 01/30/2025 → 2025-01-30
    """
    date = convert_and_extract_date(text)
    if date is not None:
        return date
    date_patterns = [
        # Day-Month-Year (30-Jan-2025) -- prioritized
        (r'\b(\d{1,2})-([A-Za-z]{3})-(\d{4})\b', lambda m: datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%d %b %Y")),

        # Quarterly patterns (Q1 2025)
        (r'(?:Q|q)([1-4])\s*(\d{4})', lambda m: datetime(int(m.group(2)), (int(m.group(1)) * 3 - 2), 1)),
        
        # Month Day, Year (January 30, 2025)
        (r'\b([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})\b', lambda m: datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y")),
        
        # Year-Month-Day (2025-01-30)
        (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        
        # Month/Day/Year (01/30/2025)
        (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', lambda m: datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))),
    ]
    
    for pattern, parser in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                date_obj = parser(match)
                return date_obj.strftime("%Y-%m-%d")
            except (ValueError, IndexError):
                continue
    
    return None

# Example usage
text = "Q2 2024 - July 23, "
date_str = extract_date_from_text(text)

print(date_str)  # Output: "2025-01-01"