import asyncio
from playwright.async_api import async_playwright
from download_transcript import download_transcript
from switch_tab import switch_tab
from download_report import download_report
from get_transcript_text import get_transcript_text
from utils.get_quarter_and_year import get_quarter_and_year
from utils.get_periodic_from_text import get_periodic_from_text
from utils.extract_date_from_text import extract_date_from_text
from utils.construct_event import construct_event
from utils.upload_to_r2 import upload_to_r2
from utils.construct_path import construct_path
from utils.remove_pdf_extension import remove_pdf_extension
from utils.classify_form_type_from_pdf import classify_form_type_from_pdf
from utils.get_non_periodic_content_type import get_non_periodic_content_type
from utils.construct_content_name import compile_content_name
from utils.extract_quarter_and_year import extract_quarter_and_year
from download_slide import download_slide
import json
import argparse
import os
import logging


async def enable_stealth(page):
    """Modify navigator to evade bot detection."""
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

if os.name == "nt":
    DEFAULT_CHROME_PATH = os.path.join("C:/", "Program Files", "Google", "Chrome", "Application", "chrome.exe")
    DEFAULT_CONFIG_PATH = r"C:\Users\Abdul Moiz Nouman\AppData\Local\Google\Chrome\User Data"
    DEFAULT_args = ["--profile-directory=Profile 1"]
else:
    DEFAULT_CHROME_PATH = "/usr/bin/google-chrome"
    DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/google-chrome")
    DEFAULT_args = ["--profile-directory=Default"]

async def scrape_event_names(ticker, url, test_run=True):
    chrome_path = os.environ.get("CHROME_PATH", DEFAULT_CHROME_PATH)
    user_data_dir = os.path.expanduser(os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH))
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename=f'logs/{ticker}_event_errors.log',  # Specify the log file name
        level=logging.ERROR,          # Set the logging level to ERROR
        format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log message format
    )

    

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        executable_path=chrome_path,
        args=DEFAULT_args,
        accept_downloads=True
    )
        page = browser.pages[0] if browser.pages else await browser.new_page()

        await enable_stealth(page)



        try:
            url = url
            print(f"Opening {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
            await page.goto('https://financialreports.eu/companies/bayer-ag/', wait_until="domcontentloaded", timeout=120000)

            print("Waiting for transcript container...")
            await page.wait_for_selector("#load-more-filings", state="visible", timeout=120000)

            # Loop to click the button until it disappears
            # while True:
            #     try:
            #         # Wait for the button to be clickable
            #         await page.wait_for_selector("#load-more-filings", state="visible", timeout=10000)
            #         # Click the button
            #         await page.click("#load-more-filings")
            #         print("Clicked 'Load More' button.")
            #         # Optionally, wait for new content to load
            #         await page.wait_for_timeout(2000)  # Adjust timeout as needed
            #     except Exception as e:
            #         print("Button no longer available or timed out.")
            #         break
            await asyncio.sleep(3)

            print("Finished loading all content.")
            rows = await page.query_selector_all("tr")
            for row in rows:
                # Extract content name
                content_name_element = await row.query_selector("div.text-xs.italic.text-gray-500.mt-0.5.line-clamp-2.break-words")
                content_name = await content_name_element.text_content() if content_name_element else "N/A"

                # Extract date
                date_element = await row.query_selector("td.hidden.md\\:table-cell.px-3.py-4.text-sm.text-gray-500.align-top.w-\\[15\\%\\] div.text-gray-900")
                date = await date_element.text_content() if date_element else "N/A"

                # Extract href
                href_element = await row.query_selector("td div.flex a.inline-flex")
                href = await href_element.get_attribute("href") if href_element else "N/A"

                print(f"Content Name: {content_name}")
                print(f"Date: {date}")
                print(f"Href: {href}")
                print("-" * 40)

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        finally:
            await browser.close()
            
asyncio.run(scrape_event_names("AAPL", "https://financialreports.eu/"))