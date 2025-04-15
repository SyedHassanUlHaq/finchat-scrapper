from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

async def download_slide(page, timeout_ms=10000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        print("Downloading slide...")
        async with page.expect_download() as download_info:
            await page.locator('(//button[@data-testid="get-file__download-button"])[last()]').click(timeout=10000)
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
        return None
    except Exception as e:
        print(f"[Report Download Error] {e}")