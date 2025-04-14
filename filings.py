import asyncio
from playwright.async_api import async_playwright
import os

async def click_load_more(page):
    """Continuously click 'Load More' until it's gone."""
    while True:
        try:
            load_more_button = await page.query_selector('button:has-text("Load More")')
            if not load_more_button:
                break
            await load_more_button.click()
            await page.wait_for_timeout(1500)  # Wait for new content to load
        except Exception as e:
            print(f"  [Load More Skipped] {e}")
            break

async def enable_stealth(page):
    """Modify navigator to evade bot detection."""
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

async def scrape_event_names():
    chrome_path = "/usr/bin/google-chrome"
    user_data_dir = os.path.expanduser("~/.config/google-chrome")
    download_dir = "/home/syed-hassan-ul-haq/repos/finchat-scrapper/downloads"

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            executable_path=chrome_path,
            args=["--profile-directory=Default"],
            accept_downloads=True
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()

        await enable_stealth(page)
        
        try:
            base_url = "https://finchat.io/company/NasdaqGS-AAPL/filings/"
            print(f"Opening {base_url}...")
            await page.goto(base_url, wait_until="domcontentloaded", timeout=120000)
            
            print("Waiting for table...")
            table_selector = "table.m_b23fa0ef.mantine-Table-table"
            await page.wait_for_selector(table_selector, timeout=20000)

            print("Scrolling to bottom to trigger loading...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            await click_load_more(page)

            # Extract and categorize events
            event_rows = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")
            if not event_rows:
                print("No events found.")
                return

            print(f"Found {len(event_rows)} event(s).")
            ten_q_k_events = []
            other_events = []

            for row in event_rows:
                tds = await row.query_selector_all("td")
                if tds:
                    event_name = await tds[0].inner_text()
                    if "10-Q" in event_name or "10-K" in event_name:
                        ten_q_k_events.append((row, event_name))
                    else:
                        other_events.append((row, event_name))

            print(f"10-Q/10-K Events: {len(ten_q_k_events)}")
            print(f"Other Events: {len(other_events)}")

            # Process both lists
            async def process_event_list(event_list, label):
                for i in range(len(event_list)):
                    print(f"\n[{label}] Processing event {i+1}/{len(event_list)}...")
                    try:
                        # Refresh the page for each iteration
                        await page.goto(base_url, wait_until="domcontentloaded")
                        await click_load_more(page)
                        await page.wait_for_selector(table_selector, timeout=20000)
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)

                        # Re-grab event list
                        updated_rows = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")
                        row, event_name = event_list[i]
                        print(f"Event Name: {event_name}")
                        await updated_rows[i].click()
                        await page.wait_for_load_state("domcontentloaded")
                        await page.wait_for_timeout(2000)

                        print("Waiting for download button...")
                        await page.wait_for_selector('button[aria-label="Download Filing"]', timeout=10000)

                        print("Triggering file download...")
                        async with page.expect_download() as download_info:
                            await page.click('button[aria-label="Download Filing"]')

                        download = await download_info.value
                        filename = download.suggested_filename
                        save_path = f"{download_dir}/{filename}"
                        await download.save_as(save_path)

                        print(f"File downloaded: {filename} → {save_path}")

                    except Exception as e:
                        print(f"  [Download Skipped] {e}")

            await process_event_list(ten_q_k_events, "10Q/10K")
            await process_event_list(other_events, "Other")

        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()
            
if __name__ == "__main__":
    asyncio.run(scrape_event_names())
