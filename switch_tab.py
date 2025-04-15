from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

async def switch_tab(page, index, timeout_ms=2000):
    """
    Extracts text from an h2 element with data-sentry-source-file="DisplayTranscriptContent.tsx".
    
    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 10s)
    
    Returns:
        str: The extracted text if found, otherwise None.
    """
    try:
        if index == 1:
            tab = 'transcript'
        elif index == 2:
            tab = 'report'
        else:
            tab = 'slides'
        print(f"Looking for {tab} tab...")
        button = page.locator(f'(//div[@class="m_89d33d6d mantine-Tabs-list"])[last()]//button[{index}]')
        # await page.click('#mantine-ik817evwu-tab-Report')
        await page.wait_for_timeout(2000)
        text = await button.inner_text()
        await button.click(timeout=2000)
        if text.lower() == 'transcript':
            return 'earnings_transcript'
        if text.lower() == 'slides':
            return 'earnings_presentation'
        if text.lower() == 'report':
            return 'earnings_press_release'
        else:
            return 'other'
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: {tab} element not found within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[{tab} Tab Switching Error] {e}")