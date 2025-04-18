import fitz  # PyMuPDF
import re

async def extract_fiscal_date(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc[0].get_text()

    match = re.search(
        r'For the (?:fiscal|quarterly) (?:year|period) ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})',
        first_page,
        re.IGNORECASE
    )
    print(f"Extracted fiscal date: {match.group(1)}")
    return match.group(1) if match else None

