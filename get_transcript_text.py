from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import asyncio

async def get_transcript_text(page, timeout_ms=10000):
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
        # await asyncio.sleep(2)
        h2_locator = page.locator('h2[data-sentry-source-file="DisplayTranscriptContent.tsx"]')
        await h2_locator.first.wait_for(state="visible", timeout=timeout_ms)


        # await asyncio.sleep(3)
        text = await h2_locator.text_content()
        
        # print('1111111111111111', text)
        # Get and return the text
        return text
    
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: h2 element not found within {timeout_ms}ms")
        return None