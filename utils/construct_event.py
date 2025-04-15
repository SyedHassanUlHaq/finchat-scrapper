import re
from datetime import datetime

def construct_event(
    equity_ticker,
    content_name,
    content_type,
    published_date,
    r2_url,
    periodicity,
    file_type = "pdf",
    geography = 'US',
    fiscal_date=None,
    fiscal_year='0000',
    fiscal_quarter='0'
):
    """
    Constructs an earnings document JSON object with smart defaults.
    
    Args:
        equity_ticker (str): Stock ticker (e.g., "AAPL")
        geography (str): Geographic region (e.g., "US")
        content_name (str): Document name (used to detect content type)
        file_type (str): File extension (e.g., "pdf")
        published_date (str): Date published in YYYY-MM-DD format
        r2_url (str): URL to the document in R2 storage
        fiscal_date (str, optional): Fiscal date in YYYY-MM-DD format
        fiscal_year (int, optional): Fiscal year
        fiscal_quarter (int, optional): Fiscal quarter (1-4)
    
    Returns:
        dict: Structured earnings document JSON object
    """
    # Determine content type from content_name
    
    
    return {
        "equity_ticker": equity_ticker.upper(),
        "geography": geography.upper(),
        "content_name": content_name,
        "file_type": file_type.lower(),
        "content_type": content_type,
        "published_date": published_date,
        "fiscal_date": fiscal_date,
        "fiscal_year": fiscal_year,
        "fiscal_quarter": fiscal_quarter,
        "r2_url": r2_url,
        "periodicity": periodicity  # Default for earnings documents
    }

# Example usage
# doc = build_earnings_document(
#     equity_ticker="AAPL",
#     geography="US",
#     content_name="Apple Inc. Transcript Jan 30 2025.pdf",
#     file_type="PDF",
#     published_date="2025-01-30",
#     r2_url="https://example.com/path/to/file.pdf"
# )

# print(doc)