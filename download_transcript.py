from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging

async def download_transcript(page, event, timeout_ms=4000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        print("Waiting for transcript download button...")
        await page.wait_for_selector("#ph-company__download-transcript", timeout=timeout_ms)
        print("Downloading transcript...")
        async with page.expect_download() as download_info:
            await page.click("#ph-company__download-transcript")
        download = await download_info.value
        filename = download.suggested_filename
        save_path = f"downloads/{filename}"
        await download.save_as(save_path)
        print(f"Transcript saved: {filename} → {save_path}")
        return filename
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: transrcipt download element not found within {timeout_ms}ms")
        logging.error(f"event: {event} Download element not found for transcript within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[Transcript Download Error] {e}")