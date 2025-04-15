import re

def identify_earnings_doc(text):
    """
    Identify the type of earnings document based on keywords in the text.
    
    Priority order:
    1. 'transcript' → 'earnings_transcript'
    2. 'report' → 'earnings_press_release'
    3. 'presentation' or 'slides' → 'earnings_presentation'
    
    Returns None if none of the keywords are found.
    """
    # Normalize the text to lowercase and remove extra spaces
    normalized_text = re.sub(r'\s+', ' ', text.lower().strip())
    
    # Check for keywords in order of priority
    if re.search(r'\btranscript\b', normalized_text):
        return 'earnings_transcript'
    elif re.search(r'\breport\b', normalized_text):
        return 'earnings_press_release'
    elif re.search(r'\b(?:presentation|slides?)\b', normalized_text):
        return 'earnings_presentation'
    else:
        return None

# Example usage
print(identify_earnings_doc("Q2 Earnings Transcript"))  # 'earnings_transcript'
print(identify_earnings_doc("Annual Report 2023"))     # 'earnings_press_release'
print(identify_earnings_doc("Investor Slides"))        # 'earnings_presentation'
print(identify_earnings_doc("Quarterly Presentation")) # 'earnings_presentation'
print(identify_earnings_doc("Financial Summary"))      # None