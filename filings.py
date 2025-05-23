import asyncio
from playwright.async_api import async_playwright
import os
import json
from datetime import datetime
from utils.upload_to_r2 import upload_to_r2
from utils.get_closest_date import find_closest_date
from utils.fiscal_date_extractor import extract_fiscal_date
from utils.get_quarter_and_year import get_quarter_and_year
from argparse import ArgumentParser

# Global list to hold metadata entries
metadata_list = []

parser = ArgumentParser(description="Scrape filings from Finchat")
parser.add_argument("ticker", type=str, help="Equity ticker to scrape filings for")
parser.add_argument("link", type=str, help="Link to scrape filings from")
parser.add_argument("json_path", type=str, help="Path to the JSON file containing dates")
args = parser.parse_args()

Equity_ticker = args.ticker
filings_link = args.link
json_path = args.json_path

async def click_load_more(page):
    while True:
        try:
            load_more_button = await page.query_selector('button:has-text("Load More")')
            if not load_more_button:
                print("  [Load More] Button not found, breaking loop.")
                break
            print("  [Load More] Clicking the button...")
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

        base_url = filings_link
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

        for row in event_rows:
            tds = await row.query_selector_all("td")
            if len(tds) >= 2:
                event_name = await tds[0].inner_text()
                event_date = await tds[1].inner_text()
                event_data = (row, event_name.strip(), event_date.strip())
                if "10-Q" in event_name or "10-K" in event_name:
                    ten_q_k_events.append(event_data)
                else:
                    other_events.append(event_data)
                        
        print("ten_q_k_events", ten_q_k_events)
        print(f"10-Q/10-K Events: {len(ten_q_k_events)}")
        print(f"Other Events: {len(other_events)}")

        async def process_event_list(event_list, label):
            for i in range(len(event_list)):
                print(f"\n[{label}] Processing event {i+1}/{len(event_list)}...")

                _, expected_event_name, expected_event_date = event_list[i]

                await page.goto(base_url, wait_until="domcontentloaded")
                print("Scrolling to bottom to trigger loading...")
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(3000)
                await click_load_more(page)
                await page.wait_for_selector(table_selector, timeout=20000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)

                updated_rows = await page.query_selector_all("tr.m_4e7aa4fd.mantine-Table-tr")

                matched_row = None
                for row in updated_rows:
                    tds = await row.query_selector_all("td")
                    if len(tds) < 2:
                        continue
                    event_name = (await tds[0].inner_text()).strip()
                    event_date = (await tds[1].inner_text()).strip()
                    if event_name == expected_event_name and event_date == expected_event_date:
                        matched_row = row
                        break

                if not matched_row:
                    print(f"⚠️ Could not find matching row for {expected_event_name} on {expected_event_date}")
                    continue

                print(f"Event Name: {expected_event_name}")
                print(f"Event Date: {expected_event_date}")
                await matched_row.click()
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
                fiscal_date = await extract_fiscal_date(save_path)

                fiscal_date = datetime.strptime(fiscal_date.replace("\xa0", " "), "%B %d, %Y") 

                closest_date = await find_closest_date(json_path, fiscal_date.strftime("%Y-%m-%d"))
                fiscal_year, fiscal_quarter = await get_quarter_and_year(closest_date)

                try:
                    event_date_obj = datetime.strptime(expected_event_date.replace("\xa0", " "), "%b %d, %Y")
                except ValueError:
                    try:
                        event_date_obj = datetime.strptime(expected_event_date.replace("\xa0", " "), "%B %d, %Y")
                    except:
                        event_date_obj = None
                published_date = event_date_obj.strftime("%Y-%m-%d") if event_date_obj else None

                r2_folder = f"{Equity_ticker}/{published_date}/{filename}/"
                r2_url = upload_to_r2(save_path, r2_folder, True)

                metadata = {
                    "equity_ticker": Equity_ticker,
                    "geography": "US",
                    "content_name": filename,
                    "file_type": "pdf",
                    "content_type": (
                        "annual_report" if "10-K" in expected_event_name.upper()
                        else "quarterly_report" if "10-Q" in expected_event_name.upper()
                        else os.path.splitext(filename)[0]
                    ),
                    "published_date": published_date,
                    "fiscal_date": fiscal_date.strftime('%Y-%m-%d'),
                    "fiscal_year": fiscal_year,
                    "fiscal_quarter": fiscal_quarter,
                    "r2_url": r2_url,
                    "periodicity": "periodic"
                }
                print(metadata)
                metadata_list.append(metadata)
        # await process_event_list(other_events, "Other")
        await process_event_list(ten_q_k_events, "10Q/10K")
        # Write all metadata to JSON file
        output_path = os.path.join(download_dir, "metadata.json")
        with open(output_path, "w") as f:
            json.dump(metadata_list, f, indent=4)
        print(f"\n📄 Metadata JSON saved to: {output_path}")

      
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_event_names())
