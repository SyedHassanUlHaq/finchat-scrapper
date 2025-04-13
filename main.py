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
    chrome_path = "/usr/bin/google-chrome"
    user_data_dir = "/home/abdulrauf/.config/google-chrome"

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

                    # --- Download transcript ---
                    try:
                        print("Waiting for transcript download button...")
                        await page.wait_for_selector("#ph-company__download-transcript", timeout=5000)

                        print("Downloading transcript...")
                        async with page.expect_download() as download_info:
                            await page.click("#ph-company__download-transcript")

                        download = await download_info.value
                        filename = download.suggested_filename
                        save_path = f"downloads/{filename}"
                        await download.save_as(save_path)
                        print(f"Transcript saved: {filename} → {save_path}")
                    except Exception as e:
                        print(f"  [Transcript Download Error] {e}")

                    # --- Try switching to Report tab ---
                    try:
                        print("Looking for Report tab...")
                        await page.locator('(//div[@class="m_89d33d6d mantine-Tabs-list"])[last()]//button[2]').click(timeout=10000)
                        # await page.click('#mantine-ik817evwu-tab-Report')
                        await page.wait_for_timeout(2000)

                        print("Waiting for Report download button...")
                        # await asyncio.sleep(5)  # Wait for the page to load
                        print("Downloading report...")
                        async with page.expect_download() as download_info:
                            await page.locator('button[data-testid="get-file__download-button"]').click(timeout=10000)
                            # await page.click(".rpv-core__minimal-button")


                        download = await download_info.value
                        filename = download.suggested_filename
                        save_path = f"downloads/{filename}"
                        await download.save_as(save_path)
                        print(f"Report saved: {filename} → {save_path}")
                    except Exception as e:
                        print(f"  [Report Download Skipped] {e}")

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
