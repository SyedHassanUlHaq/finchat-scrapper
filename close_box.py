from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import logging
import asyncio

async def close_box(page, timeout_ms=10000):
    try:
        
        await asyncio.sleep(2)
        print(f"closing box...")
        await asyncio.sleep(2)
        async with page.expect_download() as download_info:
            await page.locator(
                'footer div.mt-auto div.rounded-t-md button.mantine-focus-auto.m_8d3f4000'
            ).click(timeout=4000)
    except PlaywrightTimeoutError:
        print(f"⚠️ Error: close box  element not found within {timeout_ms}ms")
        logging.error(f"close box element not found within {timeout_ms}ms")
        return None
    except Exception as e:
        print(f"[close box Error] {e}")