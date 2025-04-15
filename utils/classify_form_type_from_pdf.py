import re
from PyPDF2 import PdfReader

def classify_form_type_from_pdf(pdf_path):
    """
    Classifies an SEC filing document based on its form type.

    Args:
        pdf_path (str): Relative file path to the PDF document.

    Returns:
        str: "quarterly report" if FORM 10-Q is matched,
             "annual report" if FORM 10-K is matched,
             "other" otherwise.
    """
    try:
        # Read the first page of the PDF
        reader = PdfReader(pdf_path)
        if len(reader.pages) == 0:
            return None  # No pages in the PDF
        
        first_page_text = reader.pages[0].extract_text()
        
        # Debugging: Print the first 500 characters of the extracted text
        # print("First 500 characters of extracted text:")
        # print(first_page_text[:500])  # Adjust the slice size as needed

        # Normalize whitespace, remove excess spaces, and handle common misinterpretations
        normalized_text = re.sub(r'\s+', ' ', first_page_text).strip().lower()
        normalized_text = normalized_text.replace("united st ates", "united states").replace("quar terly", "quarterly")
        
        # Define regex patterns for "UNITED STATES SECURITIES AND EXCHANGE COMMISSION" and form types
        sec_pattern = re.compile(r"united states\s*securities and exchange commission", re.IGNORECASE)
        quarterly_pattern = re.compile(r"form\s*10-q", re.IGNORECASE)
        annual_pattern = re.compile(r"form\s*10-k", re.IGNORECASE)

        # Check if SEC pattern is present
        if sec_pattern.search(normalized_text):
            # After SEC, check for "10-Q" or "10-K"
            if quarterly_pattern.search(normalized_text):
                return "quarterly report"
            elif annual_pattern.search(normalized_text):
                return "annual report"
        
        # Return "other" if no matches
        return "other"

    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")
        return None


# Test call
# result = classify_form_type_from_pdf("test/1.pdf")
# print(result)
# print("===" * 20)

# result = classify_form_type_from_pdf("test/2.pdf")
# print(result)
# print("===" * 20)

# result = classify_form_type_from_pdf("test/3.pdf")
# print(result)
# print("===" * 20)

# result = classify_form_type_from_pdf("test/4.pdf")
# print(result)
# print("===" * 20)

# result = classify_form_type_from_pdf("test/5.pdf")
# print(result)
# print("===" * 20)

# result = classify_form_type_from_pdf("test/6.pdf")
# print(result)
# print("===" * 20)