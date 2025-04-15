def construct_path(ticker: str, date: str, file_name: str, file: str) -> str:
    """
    Join four string parameters with '/' between them.
    
    Args:
        param1: First string
        param2: Second string
        param3: Third string
        param4: Fourth string
        
    Returns:
        String with all parameters joined by '/'
        
    Example:
        >>> join_with_slashes("a", "b", "c", "d")
        'a/b/c/d'
    """
    return f"{ticker}/{date}/{file_name}/{file}"