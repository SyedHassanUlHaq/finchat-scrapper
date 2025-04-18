def remove_pdf_extension(filename: str) -> str:
    """
    Safely removes only the .pdf/.PDF extension while preserving other dots.
    
    Args:
        filename: Input filename string
        
    Returns:
        Cleaned filename with PDF extension removed if present
        
    Examples:
        >>> remove_pdf_extension("Data.Report.PDF")
        'Data.Report'
        >>> remove_pdf_extension("notes.txt")
        'notes.txt'
    """
    if len(filename) > 4 and filename.lower().endswith('.pdf'):
        return filename[:-4]
    return filename