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
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # Enable stealth
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

                    print("Waiting for download button...")
                    await page.wait_for_selector("#ph-company__download-transcript", timeout=10000)

                    print("Downloading transcript...")
                    async with page.expect_download() as download_info:
                        await page.click("#ph-company__download-transcript")

                    download = await download_info.value
                    filename = download.suggested_filename
                    save_path = f"/home/syed-hassan-ul-haq/Downloads/{filename}"
                    await download.save_as(save_path)
                    print(f"Saved: {filename} → {save_path}")

                except Exception as e:
                    print(f"  [Download Error] {e}")

                print("Navigating back...")
                await page.go_back()
                await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"[Script Error] {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_event_names())
