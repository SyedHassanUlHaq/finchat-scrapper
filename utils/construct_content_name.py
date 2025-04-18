def compile_content_name(content_type, equity_ticker, fiscal_year, fiscal_quarter):
    # Remove underscores from content_type
    content_type_cleaned = content_type.replace('_', ' ').title()
    # Combine the parameters to form the content_name
    content_name = f"{equity_ticker} Q{fiscal_quarter} {fiscal_year} {content_type_cleaned}"
    return content_name

# Example usage
content_name = compile_content_name("earnings_transcript", "NVDA", 2025, 4)
print(content_name)  # Output: NVDA Q4 2025 Earnings Transcript
