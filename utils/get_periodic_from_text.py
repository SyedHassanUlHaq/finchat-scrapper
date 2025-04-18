import re

def get_periodic_from_text(s):
    """
    Check if a string contains periodic patterns like Q1, yyyy, etc.
    
    Args:
        s (str): Input string to check
        
    Returns:
        str: 'periodic' if periodic patterns are found, 'non_periodic' otherwise
    """
    # Define patterns that might indicate periodic data
    patterns = [
        r'\bQ[1-4]\b',      # Quarterly patterns (Q1, Q2, Q3, Q4)
        r'\bH[1-2]\b',       # Half-year patterns (H1, H2)
        # r'\bQ[1-4]\b',                # Q1, Q2, Q3, Q4
        r'\bQTR[1-4]\b',              # QTR1, QTR2, etc.
        r'\bquarter[1-4]\b',          # quarter1, quarter2, etc.
        r'\b(?:1st|2nd|3rd|4th)[- ]quarter\b',  # 1st-quarter, 2nd quarter, etc.
        r'\bquarterly\b',             # quarterly
        
        # Annual patterns
        # r'\bannual\b',                # annual
        # r'\byearly\b',                # yearly
        # r'\bYTD\b',                   # YTD (year-to-date)
        # r'\bfiscal year\b',            # fiscal year
        # r'\bFY\d{2,4}\b',             # FY23, FY2023
        
        # # Half-year patterns
        # r'\bH[1-2]\b',                # H1, H2
        # r'\b(?:1st|2nd)[- ]half\b',   # 1st-half, 2nd half
        
        # r'\byyyy\b',         # Year pattern (yyyy)
        # r'\bmm\b',           # Month pattern (mm)
        # r'\bdd\b',          # Day pattern (dd)
        # r'\bM[0-9]{1,2}\b',  # Month number (M1, M12)
        # r'\bD[0-9]{1,2}\b',  # Day number (D1, D31)
        # r'\bW[0-9]{1,2}\b',  # Week number (W1, W52)
        # r'\bS[0-9]{1,2}\b', # Season/Semester (S1, S2)
        # r'\b\d{4}\b',        # 4-digit year (2023)
        # r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',  # Month abbreviations
        # r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b'  # Full month names
    ]
    
    # Combine all patterns with OR condition
    combined_pattern = '|'.join(patterns)
    
    # Search for any of these patterns in the string (case-insensitive)
    if re.search(combined_pattern, s, flags=re.IGNORECASE):
        return 'periodic'
    else:
        return 'non_periodic'