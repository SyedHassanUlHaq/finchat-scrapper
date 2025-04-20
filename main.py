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

# from dotenv import load_dotenv
# load_dotenv()


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

async def scrape_event_names(ticker, url, test_run):
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

            print("Waiting for transcript container...")
            container_selector = "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root"
            await page.wait_for_selector(container_selector, timeout=20000)

            print("Scrolling to bottom to trigger loading...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)

            print("Fetching all event elements...")
            await asyncio.sleep(4)
            # event_links = await page.query_selector_all(
            #     "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root a"
            # )

            # if not event_links:
            #     print("No events found.")
            #     return

            download_button = await page.wait_for_selector("footer div div.mantine-Flex-root button.mantine-ActionIcon-root.mantine-UnstyledButton-root")
            await download_button.click()

            # print(f"Found {len(event_links)} event(s).")
            elements = page.locator('a#ph-company__transcripts-sidebar-item')
           # Retrieve the count of matched elements
            count = await elements.count()
            print(f"Found {count} elements with ID 'ph-company__transcripts-sidebar-item'")
            all_events = []

            for i in range(count):
                print(f"\nProcessing event {i+1}/{count}...")

                # # Re-fetch events to prevent stale references
                # event_links = await page.query_selector_all(
                #     "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root a"
                # )
                

                # if i >= len(event_links):
                #     print("  [Skipped] Event index out of range.")
                #     break

                # event = event_links[i]

                try:
                    element = elements.nth(i)
                    await element.click()
                    # await event.click()
                    await page.wait_for_load_state("domcontentloaded")
                    await page.wait_for_timeout(7000)
                    # await asyncio.sleep(4)
                    periodicity = None
                    published_date = None
                    fiscal_year = None
                    fiscal_quarter = None
                    buttons_locator = page.locator('(//div[@class="m_89d33d6d mantine-Tabs-list"])[last()]//button')
                    await page.wait_for_timeout(4000)
                    total_tabs = await buttons_locator.count()
                    print(f"total tabs in event {i}:", total_tabs)
                    for index in range(1, total_tabs + 1):
                        content_name = None
                        if index == 1:
                            heading = await get_transcript_text(page)
                            periodicity = get_periodic_from_text(heading)
                            published_date = extract_date_from_text(heading)
                            
                        # print('HEADING: ', heading, '\n\n\n')
                        content_type = await switch_tab(page, index=index, event=i) 
                        print(f"  [Content Type] {content_type}")                   

                        if content_type == "transcript":
                            # heading = await get_transcript_text(page)
                            if not heading:
                                print("  [Skipped] No heading found.")
                                continue

                            content_name = heading

                            # periodicity = get_periodic_from_text(heading)
                            # published_date = extract_date_from_text(heading)

                            print(f"  [Published Date] {published_date}")

                            transcript_name = await download_transcript(page, event=i)
                            file_name = remove_pdf_extension(transcript_name)
                            path = construct_path(ticker=ticker, date=published_date, file_name=file_name, file=transcript_name)

                            if periodicity == 'periodic':
                                content_type2 = 'earnings_transcript'
                                fiscal_quarter, fiscal_year = extract_quarter_and_year(heading)
                                content_name = compile_content_name(content_type=content_type, equity_ticker=ticker, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            else:
                                content_type2 = get_non_periodic_content_type(heading, f'downloads/{transcript_name}', content_type)
                                fiscal_year = None
                                fiscal_quarter = None
                        # content_type = "earnings_transcript"
                            pdf_type = classify_form_type_from_pdf(f'downloads/{transcript_name}')
                            r2_path = upload_to_r2(f'downloads/{transcript_name}', path, test_run=test_run)
                            if pdf_type == 'other' or pdf_type is None:
                                event = construct_event(equity_ticker=ticker, content_name=content_name, content_type=content_type2, published_date=published_date, r2_url=r2_path, periodicity=periodicity, fiscal_date=published_date, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            else:
                                event = construct_event(equity_ticker=ticker, content_name=content_name, content_type=pdf_type, published_date=published_date, r2_url=r2_path, periodicity=periodicity, fiscal_date=published_date, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            all_events.append(event)
                        elif content_type == "press_release":
                            report_name = await download_report(page, event=i)
                            file_name = remove_pdf_extension(report_name)
                            
                            if content_name is None:
                                content_name = heading
                            path = construct_path(ticker=ticker, date=published_date, file_name=file_name, file=report_name)
                            pdf_type = classify_form_type_from_pdf(f'downloads/{report_name}')
                            
                            if periodicity == 'periodic':
                                content_type2 = 'earnings_press_release'
                                content_name = compile_content_name(content_type=content_type, equity_ticker=ticker, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            else:
                                content_type2 = get_non_periodic_content_type(heading, f'downloads/{transcript_name}', content_type)

                            r2_path = upload_to_r2(f'downloads/{report_name}', path, test_run=test_run)
                            if pdf_type == 'other' or pdf_type is None:
                                event = construct_event(equity_ticker=ticker, content_name=content_name, content_type=content_type2, published_date=published_date, r2_url=r2_path, periodicity=periodicity, fiscal_date=published_date, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            else:
                                event = construct_event(equity_ticker=ticker, content_name=content_name, content_type=pdf_type, published_date=published_date, r2_url=r2_path, periodicity=periodicity, fiscal_date=published_date, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            all_events.append(event)
                        elif content_type == "presentation":
                            await asyncio.sleep(5)
                            if index == 3:
                                report_name = await download_slide(page, event=i)
                            else:
                                report_name = await download_report(page, event=i)
                            file_name = remove_pdf_extension(report_name)

                            if periodicity == 'periodic':
                                content_type2 = 'earnings_presentation'
                                content_name = compile_content_name(content_type=content_type, equity_ticker=ticker, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            else:
                                content_type2 = get_non_periodic_content_type(heading, f'downloads/{transcript_name}', content_type)
                            if content_name is None:
                                content_name = heading
                            path = construct_path(ticker=ticker, date=published_date, file_name=file_name, file=report_name)
                            r2_path = upload_to_r2(f'downloads/{report_name}', path, test_run=test_run)
                            event = construct_event(equity_ticker=ticker, content_name=content_name, content_type=content_type2, published_date=published_date, r2_url=r2_path, periodicity=periodicity, fiscal_date=published_date, fiscal_year=fiscal_year, fiscal_quarter=fiscal_quarter)
                            all_events.append(event)

                        print(f"[Event] {event}")

                        
                        #<button class="mantine-focus-auto mantine-active m_8d3f4000 mantine-ActionIcon-root m_87cf2631 mantine-UnstyledButton-root" data-variant="subtle" type="button" id="ph-company__download-transcript" style="--ai-radius: var(--mantine-radius-xs); --ai-bg: transparent; --ai-hover: var(--mantine-color-primary-light-hover); --ai-color: var(--mantine-color-primary-light-color); --ai-bd: calc(0.0625rem * var(--mantine-scale)) solid transparent;"><span class="m_8d3afb97 mantine-ActionIcon-icon"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" height="20" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M224,144v64a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V144a8,8,0,0,1,16,0v56H208V144a8,8,0,0,1,16,0Zm-101.66,5.66a8,8,0,0,0,11.32,0l40-40a8,8,0,0,0-11.32-11.32L136,124.69V32a8,8,0,0,0-16,0v92.69L93.66,98.34a8,8,0,0,0-11.32,11.32Z"></path></svg></span></button> --- Try switching to Report tab ---

                except Exception as e:
                    print(f"  [Event Error] {e}: event: {i}")
                    logging.error(f"Event Error: {e}, Event Index: {i}")



                # print("Navigating back...")
                # await page.go_back()
                # await page.wait_for_timeout(2000)
                # print()
            # Ensure the JSONS directory exists
            os.makedirs("JSONS", exist_ok=True)

            file_path = f"JSONS/{ticker}_investor_relations.json"

            # Write the list of dictionaries to a JSON file
            with open(file_path, 'w') as json_file:
                json.dump(all_events, json_file, indent=4)

            print(f"JSON file has been created at {file_path}")
            logging.error(f"{len(all_events)} out of {count} processed for equity {ticker}")

        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape event names with provided arguments.")

    # Add arguments to the parser
    parser.add_argument("ticker", type=str, help="equity ticker")
    parser.add_argument("url", type=str, help="page url")
    parser.add_argument("test_run", type=str, help="test run")

    # Parse the arguments from the command line
    args = parser.parse_args()

    asyncio.run(scrape_event_names(args.ticker, args.url, args.test_run))