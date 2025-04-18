import re

def check_cagny(text, path):
    # Define the regular expression pattern to match 'CAGNY'
    pattern = r'\bCAGNY\b'
    # Search for the pattern in the text
    found = bool(re.search(pattern, text, re.IGNORECASE))
    if found:
        return True
    return contains_cagny_in_pdf(path)

# Example usage
# print(contains_cagny("This is a test string with CAGNY in it."))          # Output: True
# print(contains_cagny("This string does not contain the word."))           # Output: False
# print(contains_cagny("Check this (CAGNY) example."))                      # Output: True
# print(contains_cagny("CAGNY can be anywhere in the text."))               # Output: True
# print(contains_cagny("This has cagny but not in uppercase."))             # Output: True

import fitz  # PyMuPDF
import re

def contains_cagny_in_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    # Define the regular expression pattern to match 'CAGNY'
    pattern = r'\bCAGNY\b'

    # Loop through the first 5 pages or fewer if the PDF has less
    for page_number in range(min(5, len(pdf_document))):
        page = pdf_document.load_page(page_number)
        text = page.get_text()
        # Search for the pattern in the text
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False

# Example usage
# print(contains_cagny_in_pdf("path/to/your/pdf_file.pdf"))
