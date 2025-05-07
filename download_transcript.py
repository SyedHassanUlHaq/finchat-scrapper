from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging
import asyncio

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
        retries = 4
        for attempt in range(1, retries + 1):
            try:
                print("Waiting for transcript download button...")
                await page.wait_for_selector(
                    "div.hidden.w-full div.flex div.relative.m_7485cace.mantine-Container-root div.m_6d731127 div.hide-scrollbar div.m_7485cace div.m_8bffd616 div.rounded-b-none.m_e615b15f div.m_4451eb3a button#ph-company__download-transcript",
                    timeout=timeout_ms
                )
                print("Downloading transcript...")
                async with page.expect_download() as download_info:
                    await page.click(
                    "div.hidden.w-full div.flex div.relative.m_7485cace.mantine-Container-root div.m_6d731127 div.hide-scrollbar div.m_7485cace div.m_8bffd616 div.rounded-b-none.m_e615b15f div.m_4451eb3a button#ph-company__download-transcript"
                    )
                download = await download_info.value
                filename = download.suggested_filename
                save_path = f"downloads/{filename}"
                await download.save_as(save_path)
                print(f"Transcript saved: {filename} → {save_path}")
                return filename
            except PlaywrightTimeoutError as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt < retries:
                    print("Retrying in 2 seconds...")
                    await asyncio.sleep(2)
                else:
                    raise
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: transrcipt download element not found within {timeout_ms}ms")
        logging.error(f"event: {event} Download element not found for transcript within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[Transcript Download Error] {e}")