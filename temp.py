import asyncio
from playwright.async_api import async_playwright


async def enable_stealth(page):
    """Modify navigator to evade bot detection."""
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)


async def scrape_event_names():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await enable_stealth(page)

        try:
            url = "https://finchat.io/company/NasdaqGS-AAPL/investor-relations/"
            print(f"Opening {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)

            print("Waiting for transcript container...")
            container_selector = "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root"
            await page.wait_for_selector(container_selector, timeout=20000)

            # Force scroll to bottom to trigger lazy loading
            print("Scrolling to bottom to trigger loading...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)  # give it time to load

            print("Fetching all transcript/event elements...")
            event_elements = await page.query_selector_all(
                "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root a div.m_f07af9d2.mantine-NavLink-body"
            )

            if not event_elements:
                print("No event names found.")
                return

            print(f"Found {len(event_elements)} event(s):")
            for el in event_elements:
                text = await el.inner_text()
                print(f" - {text}")

        except Exception as e:
            print(f"[Error] {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_event_names())
