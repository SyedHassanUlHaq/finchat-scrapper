from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging

async def switch_tab(page, index, event, timeout_ms=2000):
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
        # button = page.locator(f'(//div[@class="m_89d33d6d mantine-Tabs-list"])[last()]//button[{index}]')
        button = await page.query_selector_all(f'div.hidden.w-full div.flex div.relative.m_7485cace.mantine-Container-root div.m_6d731127 div.hide-scrollbar div.m_7485cace div.m_8bffd616 div.hidden div.m_89d60db1.mantine-Tabs-root div.m_89d33d6d.mantine-Tabs-list button')
        # button = await page.query_selector_all(f'div.hidden.w-full.m_8bffd616 div div div div div ')
        # print('length', len(button))
        # print('button', button[0])
        # c = 0
        # for b in button:
        #     t = await b.inner_text()
        #     print(f'button_index: {c}', t)
        #     c +=1
        
        # await page.click('#mantine-ik817evwu-tab-Report')
        # await page.wait_for_timeout(10000)

        text = await button[index - 1].inner_text()
        print('text', text)
        await button[index - 1].click(timeout=10000)
        if text.lower() == 'transcript':
            return 'transcript'
        if text.lower() == 'slides':
            return 'presentation'
        if text.lower() == 'report':
            return 'press_release'
        else:
            return 'other'
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: {tab} element not found within {timeout_ms}ms")
        logging.error(f"event: {event} element {index} not found within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[{tab} Tab Switching Error] {e}")