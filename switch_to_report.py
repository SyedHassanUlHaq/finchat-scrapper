from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

async def switch_to_report(page, timeout_ms=10000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        print("Looking for Report tab...")
        await page.locator('(//div[@class="m_89d33d6d mantine-Tabs-list"])[last()]//button[2]').click(timeout=10000)
        # await page.click('#mantine-ik817evwu-tab-Report')
        await page.wait_for_timeout(2000)
        return True
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: report element not found within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[Report Tab Switching Error] {e}")