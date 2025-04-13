from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def download_transcript(page, timeout_ms=10000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        # Wait for the h2 element to be visible
        h2_locator = page.locator('h2[data-sentry-source-file="DisplayTranscriptContent.tsx"]')
        h2_locator.first.wait_for(state="visible", timeout=timeout_ms)
        
        # Get and return the text
        return h2_locator.text_content()
    
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: h2 element not found within {timeout_ms}ms")
        return None