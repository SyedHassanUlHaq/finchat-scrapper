import asyncio
from playwright.async_api import async_playwright
from download_transcript import download_transcript
from switch_to_report import switch_to_report
from download_report import download_report
from get_transcript_text import get_transcript_text
from utils.get_quarter_and_year import get_quarter_and_year
from utils.get_periodic_from_text import get_periodic_from_text
from utils.extract_date_from_text import extract_date_from_text
import os

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
            url = "https://finchat.io/company/NasdaqGS-AAPL/investor-relations/"
            print(f"Opening {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)

            print("Waiting for transcript container...")
            container_selector = "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root"
            await page.wait_for_selector(container_selector, timeout=20000)

            print("Scrolling to bottom to trigger loading...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)

            print("Fetching all event elements...")
            event_links = await page.query_selector_all(
                "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root a"
            )

            if not event_links:
                print("No events found.")
                return

            print(f"Found {len(event_links)} event(s).")

            for i in range(len(event_links)):
                print(f"\nProcessing event {i+1}/{len(event_links)}...")

                # Re-fetch events to prevent stale references
                event_links = await page.query_selector_all(
                    "div.m_e615b15f.mantine-Card-root.m_1b7284a3.mantine-Paper-root a"
                )

                if i >= len(event_links):
                    print("  [Skipped] Event index out of range.")
                    break

                event = event_links[i]

                try:
                    await event.click()
                    await page.wait_for_load_state("domcontentloaded")
                    await page.wait_for_timeout(2000)

                    heading = await get_transcript_text(page)
                    if not heading:
                        print("  [Skipped] No heading found.")
                    
                    print(heading)
                    periodicity = get_periodic_from_text(heading)
                    published_date = extract_date_from_text(heading)
                    if periodicity == 'periodic':
                        fiscal_year, fiscal_quarter = get_quarter_and_year(heading)
                    else:
                        fiscal_year = "0000"
                        fiscal_quarter = "0"
                    



                    transcript_name = await download_transcript(page)

                    #<button class="mantine-focus-auto mantine-active m_8d3f4000 mantine-ActionIcon-root m_87cf2631 mantine-UnstyledButton-root" data-variant="subtle" type="button" id="ph-company__download-transcript" style="--ai-radius: var(--mantine-radius-xs); --ai-bg: transparent; --ai-hover: var(--mantine-color-primary-light-hover); --ai-color: var(--mantine-color-primary-light-color); --ai-bd: calc(0.0625rem * var(--mantine-scale)) solid transparent;"><span class="m_8d3afb97 mantine-ActionIcon-icon"><svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 256 256" height="20" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M224,144v64a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V144a8,8,0,0,1,16,0v56H208V144a8,8,0,0,1,16,0Zm-101.66,5.66a8,8,0,0,0,11.32,0l40-40a8,8,0,0,0-11.32-11.32L136,124.69V32a8,8,0,0,0-16,0v92.69L93.66,98.34a8,8,0,0,0-11.32,11.32Z"></path></svg></span></button> --- Try switching to Report tab ---
                    switch = await switch_to_report(page)
                    if switch:
                        report_name = await download_report(page)
                    else:
                        print("Report tab not found, skipping...")
                        continue

                except Exception as e:
                    print(f"  [Event Error] {e}")

                print("Navigating back...")
                await page.go_back()
                await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_event_names())
