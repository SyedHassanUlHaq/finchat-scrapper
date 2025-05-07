from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging
import asyncio

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
        print("Waiting for report download button...")
        retries = 4
        await asyncio.sleep(2)
        for attempt in range(retries):
            d_button = await page.query_selector_all(
            "div.hidden.w-full div.flex div.relative.m_7485cace.mantine-Container-root div.m_6d731127 div.hide-scrollbar div.m_7485cace div.m_8bffd616 div.rounded-b-none.m_e615b15f div.m_4451eb3a button#ph-company__download-report span"
            )
            print(f"Attempt {attempt + 1}: Found {len(d_button)} download buttons")
            if d_button:
                break
            if attempt < retries - 1:
                await asyncio.sleep(2)
        else:
            print("Download button not found after retries.")
            return None

        print("Downloading report...")
        await asyncio.sleep(3)

        retries = 4
        for attempt in range(retries):
            try:
                async with page.expect_download() as download_info:
                    await d_button[0].click(timeout=timeout_ms)
                break  # If click succeeds, exit retry loop
            except Exception as e:
                print(f"Attempt {attempt + 1}: Download click failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(2)
                else:
                    print("Failed to trigger download after retries.")
                    raise PlaywrightTimeoutError
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