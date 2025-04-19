from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging

async def download_report(page, event, timeout_ms=10000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        print("Downloading report...")
        async with page.expect_download() as download_info:
            await page.locator('button[data-testid="get-file__download-button"]').click(timeout=5000)
            # await page.click(".rpv-core__minimal-butto
        download = await download_info.value
        filename = download.suggested_filename
        save_path = f"downloads/{filename}"
        await download.save_as(save_path)
        print(f"Report saved: {filename} → {save_path}")
        return filename
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: report Download element not found within {timeout_ms}ms")
        logging.error(f"event: {event} Download element not found for report within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[Report Download Error] {e}")