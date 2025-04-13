from datetime import datetime

def get_quarter_and_year(date_input):
    """
    Returns the year and quarter for a given date in the format 'QX-YYYY'
    
    Parameters:
    - date_input: datetime.date, datetime.datetime, or string in YYYY-MM-DD format
    
    Returns:
    - str: e.g., 'Q1-2024'
    """
    if isinstance(date_input, str):
        date_input = datetime.strptime(date_input, "%Y-%m-%d")
    
    year = date_input.year
    month = date_input.month
    
    if 1 <= month <= 3:
        quarter = "Q1"
    elif 4 <= month <= 6:
        quarter = "Q2"
    elif 7 <= month <= 9:
        quarter = "Q3"
    elif 10 <= month <= 12:
        quarter = "Q4"
    else:
        raise ValueError("Invalid month value.")
    
    return year, quarter
