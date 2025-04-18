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
    if match:
        fiscal_date = match.group(1)
        print(f"✅ Extracted fiscal date: {fiscal_date}")
        return fiscal_date
    else:
        print(f"⚠️ No fiscal date found in: {pdf_path}")
        return None
