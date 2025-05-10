from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging
import asyncio

async def download_slide(page, event, timeout_ms=10000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        max_retries = 4
        await asyncio.sleep(2)
        for attempt in range(1, max_retries + 1):
            try:
                print(f"Downloading slide... (Attempt {attempt})")
                await asyncio.sleep(2)
                async with page.expect_download() as download_info:
                    await page.locator(
                        'div.hidden.w-full div.flex div.relative.m_7485cace.mantine-Container-root div.m_6d731127 div.hide-scrollbar div.m_7485cace div.m_8bffd616 div.rounded-b-none.m_e615b15f div.m_4451eb3a button#ph-company__download-report'
                    ).click(timeout=8000)
                break  # Exit loop if successful
            except PlaywrightTimeoutError as e:
                if attempt == max_retries:
                    raise Exception # Let the outer try/except handle the final failure
                print(f"Retrying download... ({attempt}/{max_retries})")
            # button = page.locator('button[data-testid="get-file__download-button"]')
            # await page.wait_for_timeout(5000)
            # if button:
            #     last_button = await button.last()
            #     if last_button:
            #         last_button.click()
            # await page.locator('button[data-testid="get-file__download-button"]').last().click(timeout=10000)
            # await page.click(".rpv-core__minimal-butto
        download = await download_info.value
        filename = download.suggested_filename
        save_path = f"downloads/{filename}"
        await download.save_as(save_path)
        print(f"slide saved: {filename} → {save_path}")
        return filename
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: slide Download element not found within {timeout_ms}ms")
        logging.error(f"event: {event} Download element not found for slide within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[Slide Download Error] {e}")