import re
import fitz  # PyMuPDF
from format_date import format_date

def extract_fiscal_year_date(pdf_path):
    # Open the PDF using PyMuPDF
    document = fitz.open(pdf_path)

    # Regex patterns for extracting fiscal year dates with variations
    date_patterns = [
        r'From the fiscal year ended (\w+ \d{1,2}, \d{4})',  # matches "From the fiscal year ended January 26, 2025"
        r'Fiscal year ended (\w+ \d{1,2}, \d{4})',  # matches "Fiscal year ended January 26, 2025"
        r'Ended (\w+ \d{1,2}, \d{4})',  # matches "Ended January 26, 2025"
        # r'\b(\w+ \d{1,2}, \d{4})\b'  # just the date (to catch "January 26, 2025" in any context)
    ]
    
    # Loop through all pages of the PDF and extract the text
    extracted_dates = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        # Search for the patterns on the text extracted from the page
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)  # Append the extracted date

    return extracted_dates

# Example usage:
# pdf_path = "0001045810-25-000023.pdf"
# dates = extract_fiscal_year_date(pdf_path)

# print(format_date(dates))
