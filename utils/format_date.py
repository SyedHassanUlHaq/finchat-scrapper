from datetime import datetime

def format_date(date_str):
    """
    Takes a date string and converts it to 'YYYY-MM-DD' format.
    Tries multiple common input formats.
    Returns None if format is unrecognized.
    """
    possible_formats = [
        "%B %d, %Y",     # e.g., March 19, 2025
        "%b %d, %Y",     # e.g., Mar 19, 2025
        "%d %B %Y",      # e.g., 19 March 2025
        "%d %b %Y",      # e.g., 19 Mar 2025
        "%Y-%m-%d",      # already in correct format
        "%m/%d/%Y",      # e.g., 03/19/2025
        "%d/%m/%Y",      # e.g., 19/03/2025
        "%Y/%m/%d",      # e.g., 2025/03/19
        "%Y.%m.%d",      # e.g., 2025.03.19
        "%d-%b-%Y",      # e.g., 19-Mar-2025
        "%d-%B-%Y",      # e.g., 19-March-2025
    ]

    for fmt in possible_formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None