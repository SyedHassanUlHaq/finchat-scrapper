import os
import aiofiles
import aiohttp
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
from bs4 import BeautifulSoup
import json
from datetime import datetime
from utils.upload_to_r2 import upload_to_r2
from utils.fiscal_date_extractor import extract_fiscal_date
from urllib.parse import urlparse

DOWNLOAD_DIR = "downloads"
JSONS_DIR = "JSONS"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(JSONS_DIR, exist_ok=True)

def date_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def make_serializable(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, dict):
        return {key: make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)

async def save_results_to_json(data, equity_ticker):
    try:
        serializable_data = make_serializable(data)
        filename = f"{equity_ticker}_sec_filings.json"
        async with aiofiles.open(os.path.join(JSONS_DIR, filename), "w") as json_file:
            await json_file.write(json.dumps(serializable_data, indent=4))
        print(f"✅ Data saved to {JSONS_DIR}/{filename}")
    except Exception as e:
        print(f"⚠️ Failed to save JSON file: {e}")

async def accept_cookies(page):
    try:
        cookie_button = await page.query_selector("button:has-text('Accept')")
        if cookie_button:
            await cookie_button.click()
            await asyncio.sleep(2)
            print("✅ Accepted cookies.")
    except Exception:
        print("⚠️ No cookie banner or error clicking. Continuing...")

async def enable_stealth(page):
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    """)

async def click_next_page(page):
    try:
        next_button = await page.query_selector("li.pager__item--next a")
        if next_button:
            await next_button.click()
            await asyncio.sleep(3)
            return True
    except PlaywrightTimeoutError:
        print("⚠️ Timeout clicking next page.")
    except Exception as e:
        print(f"⚠️ Error clicking next page: {e}")
    return False

async def scroll_page(page):
    try:
        last_height = await page.evaluate("document.body.scrollHeight")
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("✅ Finished scrolling.")
    except Exception as e:
        print(f"⚠️ Error during scrolling: {e}")

async def load_page(page, url, block_selector):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await accept_cookies(page)
        await enable_stealth(page)
        await page.wait_for_selector(block_selector, timeout=15000)
        await scroll_page(page)
    except PlaywrightTimeoutError:
        print(f"⚠️ Timeout loading page or waiting for selector {block_selector}")
    except Exception as e:
        print(f"⚠️ Error loading page: {e}")

async def _extract_inner_html(page, block_selector):
    try:
        blocks = await page.query_selector_all(block_selector)
        html_blocks = [await page.evaluate('(element) => element.outerHTML', block) for block in blocks if block]
        print(f"📦 Found {len(html_blocks)} blocks")
        return html_blocks
    except Exception as e:
        print(f"⚠️ Error extracting HTML blocks: {e}")
        return []

async def download_pdf(session, url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # 👉 Force ".pdf" extension
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    file_path = os.path.join(DOWNLOAD_DIR, filename)

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            resp.raise_for_status()
            async with aiofiles.open(file_path, mode='wb') as f:
                await f.write(await resp.read())
        return file_path, filename
    except Exception as e:
        print(f"⚠️ Failed downloading PDF {url}: {e}")
        return None, None

def find_first_10k_index(filings):
    for index, filing in enumerate(filings):
        if filing.get('content_type') == 'annual_report':
            pub_date = filing['published_date']
            if isinstance(pub_date, str):
                year = int(pub_date[:4])
            else:
                year = pub_date.year
            return index, year
    return -1, None

def map_value(value):
    mapping = {0: 0, 1: 3, 2: 2, 3: 1}
    return mapping.get(value, 0)

async def parse_filing_block(session, html, equity_ticker, latest_year, quarter_index, quarter_cycle, test_run='true'):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        # 1. Filing Date
        filing_date_tag = soup.select_one("td.views-field-field-nir-sec-date-filed time")
        if not filing_date_tag:
            print("⚠️ No filing date found.")
            return None
        filing_date_raw = filing_date_tag.get_text(strip=True)
        print(f"📅 Filing Date Raw: {filing_date_raw}")

        published_date = datetime.strptime(filing_date_raw, "%b %d, %Y").date()

        # 2. Filing Type
        filing_type_tag = soup.select_one("td.views-field-field-nir-sec-form a")
        if not filing_type_tag:
            print("⚠️ No filing type link found.")
            return None
        filing_type = filing_type_tag.get_text(strip=True).upper()
        print(f"📝 Filing Type: {filing_type}")

        # ✅ Instead of checking only 10-K/10-Q, now allow all types (like 8-K, etc.)
        # If you want to filter some forms, add a condition here.

        # 3. PDF Link
        pdf_link_tag = soup.select_one("td.views-field-nothing-1 div.file-link span.file--mime-application-pdf a")
        if not pdf_link_tag:
            print("⚠️ No PDF link found.")
            return None

        pdf_href = pdf_link_tag.get('href')
        if not pdf_href:
            print("⚠️ PDF link missing href.")
            return None

        if pdf_href.startswith("//"):
            pdf_url = "https:" + pdf_href
        elif pdf_href.startswith("/"):
            pdf_url = "https://ir.appliedmaterials.com" + pdf_href
        else:
            pdf_url = pdf_href

        print(f"🔗 PDF URL: {pdf_url}")

        file_path, filename = await download_pdf(session, pdf_url)
        if not file_path:
            print("⚠️ Failed to download the PDF file.")
            return None

        r2_url = upload_to_r2(file_path, f"{equity_ticker}/{published_date}/{filename}", test_run=test_run)
        print(f"☁️ Uploaded to R2: {r2_url}")

        # Fiscal date extraction
        fiscal_date_raw = await extract_fiscal_date(file_path)
        fiscal_date = datetime.strptime(fiscal_date_raw, "%B %d, %Y").date() if fiscal_date_raw else None

        fiscal_year = int(fiscal_date.year) if fiscal_date and quarter_cycle[quarter_index] == 4 else latest_year
        fiscal_quarter = quarter_cycle[quarter_index]

        content_name = f"{equity_ticker} Q{fiscal_quarter} {fiscal_year} {filing_type}"

        return {
            "equity_ticker": equity_ticker,
            "geography": "US",
            "content_name": content_name,
            "file_type": "pdf",
            "content_type": "other_filing",  # because it could be 8-K, etc.
            "published_date": published_date,
            "fiscal_date": fiscal_date.isoformat() if fiscal_date else None,
            "fiscal_year": fiscal_year,
            "fiscal_quarter": fiscal_quarter,
            "r2_url": r2_url,
            "periodicity": "unscheduled" if filing_type == "8-K" else "periodic"
        }
    except Exception as e:
        print(f"⚠️ Error parsing filing block: {e}")
        return None

async def scrape(url, equity_ticker, block_selector, test_run='true'):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async with aiohttp.ClientSession() as session:
            try:
                print(f"🔍 Navigating to: {url}")
                await load_page(page, url, block_selector)
                print("✅ Page loaded")

                all_results = []
                page_num = 1
                quarter_cycle = [4, 3, 2, 1]
                latest_year = None
                quarter_index = 0

                while True:
                    print(f"\n📄 Scraping page {page_num}")
                    events = await _extract_inner_html(page, block_selector)

                    filings = []
                    for event_html in events:
                        parsed = await parse_filing_block(session, event_html, equity_ticker, latest_year, quarter_index, quarter_cycle, test_run)
                        if parsed:
                            filings.append(parsed)

                    if latest_year is None and filings:
                        ind, latest_year = find_first_10k_index(filings)
                        quarter_index = map_value(ind)
                        if ind != 0:
                            latest_year += 1

                    all_results.extend(filings)
                    quarter_index = (quarter_index + len(filings)) % len(quarter_cycle)

                    print(f"✅ Scraped {len(filings)} filings from page {page_num}")

                    success = await click_next_page(page)
                    if not success:
                        print("✅ No more pages to scrape.")
                        break

                    page_num += 1

                print(f"\n📦 Total filings scraped: {len(all_results)}")
                await save_results_to_json(all_results, equity_ticker)

            except Exception as e:
                print(f"⚠️ Fatal error during scraping: {e}")

        await browser.close()

if __name__ == "__main__":
    url = "https://www.asml.com/en/investors/shares/sec-filings"
    equity_ticker = "ASML"  # Correct ticker for Applied Materials
    block_selector = "table.nirtable.views-table.views-view-table.cols-5 tbody tr"

    asyncio.run(scrape(url, equity_ticker, block_selector))
