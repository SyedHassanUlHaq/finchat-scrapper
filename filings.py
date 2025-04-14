import asyncio
from playwright.async_api import async_playwright

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
    user_data_dir = "/home/syed-hassan-ul-haq/.config/google-chrome"

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

            # Initial fetch
            event_links = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")

            if not event_links:
                print("No events found.")
                return

            print(f"Found {len(event_links)} event(s).")

            for i in range(len(event_links)):
                print(f"\nProcessing event {i+1}/{len(event_links)}...")

                try:
                    # Re-fetch event rows to avoid stale references
                    await page.goto(base_url, wait_until="domcontentloaded")
                    await click_load_more(page)
                    await page.wait_for_selector(table_selector, timeout=20000)
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)
                    event_links = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")

                    # Print the first <td>'s text content
                    first_td = await event_links[i].query_selector("td")
                    if first_td:
                        event_name = await first_td.inner_text()
                        print(f"Event Name: {event_name}")
                    else:
                        print("  [First TD Not Found]")

                    # Click on the event row
                    await event_links[i].click()
                    await page.wait_for_load_state("domcontentloaded")
                    await page.wait_for_timeout(2000)

                    print("Waiting for download button...")
                    await page.wait_for_selector('button[aria-label="Download Filing"]', timeout=10000)

                    print("Triggering file download...")
                    async with page.expect_download() as download_info:
                        await page.click('button[aria-label="Download Filing"]')

                    download = await download_info.value
                    filename = download.suggested_filename
                    save_path = f"/home/syed-hassan-ul-haq/repos/finchat-scrapper/downloads/{filename}"
                    await download.save_as(save_path)

                    print(f"File downloaded: {filename} → {save_path}")

                except Exception as e:
                    print(f"  [Report Download Skipped] {e}")
        
        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_event_names())
