import re
from datetime import datetime

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
    date_patterns = [
        # Quarterly patterns (Q1 2025)
        (r'(?:Q|q)([1-4])\s*(\d{4})', lambda m: datetime(int(m.group(2)), (int(m.group(1)) * 3 - 2), 1)),
        
        # Month Day, Year (January 30, 2025)
        (r'\b([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})\b', lambda m: datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y")),
        
        # Day-Month-Year (30-Jan-2025)
        (r'\b(\d{1,2})-([A-Za-z]{3})-(\d{4})\b', lambda m: datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%d %b %Y")),
        
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
# text = "Q1 2025 - January 30, 2025"
# date_str = extract_first_date(text)
# print(date_str)  # Output: "2025-01-01"