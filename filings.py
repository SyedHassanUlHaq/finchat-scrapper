import asyncio
from playwright.async_api import async_playwright
import os
import json
from datetime import datetime
from utils.upload_to_r2 import upload_to_r2
# Global list to hold metadata entries
metadata_list = []

async def smart_load_more(page, row_selector, max_clicks=13):
    for _ in range(max_clicks):
        old_count = len(await page.query_selector_all(row_selector))
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        load_more = await page.query_selector('button:has-text("Load More")')
        if load_more:
            await load_more.click()
        await page.wait_for_timeout(1500)
        new_count = len(await page.query_selector_all(row_selector))
        if new_count == old_count:
            break
        
async def click_load_more(page):
    for i in range(16):
        try:
            load_more_button = await page.query_selector('button:has-text("Load More")')
            if not load_more_button:
                break
            await load_more_button.click()
            await page.wait_for_timeout(1500)
        except Exception as e:
            print(f"  [Load More Skipped] {e}")
            break

async def enable_stealth(page):
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

async def scrape_event_names():
    chrome_path = "/usr/bin/google-chrome"
    user_data_dir = os.path.expanduser("~/.config/google-chrome")
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)

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
            base_url = "https://finchat.io/investor/procter-gamble-co/filings/"
            print(f"Opening {base_url}...")
            await page.goto(base_url, wait_until="domcontentloaded", timeout=120000)

            print("Waiting for table...")
            table_selector = "table.m_b23fa0ef.mantine-Table-table"
            await page.wait_for_selector(table_selector, timeout=20000)

            print("Scrolling to bottom to trigger loading...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            await click_load_more(page)

            event_rows = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")
            if not event_rows:
                print("No events found.")
                return

            print(f"Found {len(event_rows)} event(s).")
            ten_q_k_events = []
            other_events = []

            cutoff_date = datetime.now().replace(year=datetime.now().year - 10)

            for row in event_rows:
                tds = await row.query_selector_all("td")
                if len(tds) >= 2:
                    event_name = await tds[0].inner_text()
                    event_date = await tds[1].inner_text()
                    event_date_str = event_date.strip()
                    try:
                        event_date_obj = datetime.strptime(event_date_str, "%b %d, %Y")
                    except ValueError:
                        try:
                            event_date_obj = datetime.strptime(event_date_str, "%B %d, %Y")
                        except:
                            continue  # Skip rows with unknown date format
                        
                    if event_date_obj < cutoff_date:
                        continue  # Skip events older than 10 years
                    
                    event_data = (row, event_name.strip(), event_date_str)
                    if "10-Q" in event_name or "10-K" in event_name:
                        ten_q_k_events.append(event_data)
                    else:
                        other_events.append(event_data)

            print(f"10-Q/10-K Events: {len(ten_q_k_events)}")
            print(f"Other Events: {len(other_events)}")

            async def process_event_list(event_list, label):
                for i in range(len(event_list)):
                    print(f"\n[{label}] Processing event {i+1}/{len(event_list)}...")
                    try:
                        await page.goto(base_url, wait_until="domcontentloaded")
                        await click_load_more(page)
                        await page.wait_for_selector(table_selector, timeout=20000)
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)

                        updated_rows = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")
                        row, event_name, event_date_raw = event_list[i]
                        print(f"Event Name: {event_name}")
                        print(f"Event Date: {event_date_raw}")
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
                        save_path = os.path.join(download_dir, filename)
                        await download.save_as(save_path)

                        for _ in range(20):
                            if os.path.exists(save_path):
                                break
                            await asyncio.sleep(0.5)

                        if os.path.exists(save_path):
                            print(f"✅ File downloaded: {filename} → {save_path}")
                        else:
                            print(f"❌ Download failed or file not saved: {filename}")

                        # Format date and extract fiscal info
                        try:
                            event_date_obj = datetime.strptime(event_date_raw, "%b %d, %Y")
                        except ValueError:
                            try:
                                event_date_obj = datetime.strptime(event_date_raw, "%B %d, %Y")
                            except:
                                event_date_obj = None

                        published_date = event_date_obj.strftime("%Y-%m-%d") if event_date_obj else None
                        fiscal_quarter = (event_date_obj.month - 1) // 3 + 1 if event_date_obj else 1
                        r2_folder = f"AAPL/{published_date}/{filename}/"
                        r2_url = upload_to_r2(save_path, r2_folder, False)
                        
                        metadata = {
                            "equity_ticker": "PG",
                            "geography": "US",
                            "content_name": filename,
                            "file_type": "pdf",
                            "content_type": os.path.splitext(filename)[0],
                            "published_date": published_date,
                            "fiscal_date": published_date,
                            "fiscal_year": "0000",
                            "fiscal_quarter": fiscal_quarter,
                            "r2_url": r2_url,
                            "periodicity": "non-periodic"
                        }
                        metadata_list.append(metadata)

                    except Exception as e:
                        print(f"  [Download Skipped] {e}")

            await process_event_list(other_events, "Other")
            # await process_event_list(ten_q_k_events, "10Q/10K")

            # Write all metadata to JSON file
            output_path = os.path.join(download_dir, "metadata.json")
            with open(output_path, "w") as f:
                json.dump(metadata_list, f, indent=4)
            print(f"\n📄 Metadata JSON saved to: {output_path}")

        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_event_names())
