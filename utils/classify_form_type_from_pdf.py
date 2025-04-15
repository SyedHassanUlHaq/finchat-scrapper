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

        # Normalize whitespace and make the text case-insensitive
        normalized_text = re.sub(r'\s+', ' ', first_page_text).strip().lower()

        # Define regex patterns for 10-Q and 10-K
        quarterly_pattern = re.compile(r"form\s*10-q", re.IGNORECASE)
        annual_pattern = re.compile(r"form\s*10-k", re.IGNORECASE)


        # Match patterns
        if quarterly_pattern.search(normalized_text):
            return "quarterly report"
        elif annual_pattern.search(normalized_text):
            return "annual report"
        else:
            return "other"

    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")
        return "other"

# Test call
result = classify_form_type_from_pdf("test/1.pdf")
print("Classification result:", result)

result = classify_form_type_from_pdf("test/2.pdf")
print("Classification result:", result)

result = classify_form_type_from_pdf("test/3.pdf")
print("Classification result:", result)

result = classify_form_type_from_pdf("test/4.pdf")
print("Classification result:", result)
