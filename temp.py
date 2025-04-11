from playwright.async_api import async_playwright
import os
import asyncio

# Custom Stealth function to modify the navigator object to evade bot detection
async def enable_stealth(page):
    """Inject JavaScript to evade bot detection."""
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

# Function to scrape the data and download the transcript
async def scrape_transcripts():
    async with async_playwright() as p:
        # Launch browser in headless mode temporarily for better visibility
        browser = await p.chromium.launch(headless=False)  # Set headless=False to see the browser
        
        # Create a new context with download acceptance
        browser_context = await browser.new_context(accept_downloads=True)  # Enable downloads
        page = await browser_context.new_page()
        
        # Apply stealth injection to avoid detection
        await enable_stealth(page)
        
        try:
            # Navigate to the desired URL and wait until "domcontentloaded" with an increased timeout
            await page.goto("https://finchat.io/company/NasdaqGS-AAPL/investor-relations/", wait_until="domcontentloaded", timeout=120000)  # Timeout set to 120 seconds
            
            # Wait for the specific transcript link to appear
            transcript = await page.wait_for_selector("div.m_e615b15f a.mantine-focus-auto.m_f0824112.mantine-NavLink-root.m_87cf2631.mantine-UnstyledButton-root")
            
            if transcript:
                # Extract the title from the specific transcript tag
                title = await transcript.query_selector("div.m_f07af9d2.mantine-NavLink-body")
                title_text = await title.inner_text() if title else 'No Title'
                
                print(f"Title: {title_text}")
            else:
                print("Specific transcript link not found!")
                return

            # Wait for the download button to appear
            download_button = await page.wait_for_selector("button.mantine-focus-auto.mantine-active.m_8d3f4000.mantine-ActionIcon-root.m_87cf2631.mantine-UnstyledButton-root")

            if download_button:
                # Listen for download event to save the file locally
                print("Download button found, preparing to download...")
                download_folder = os.path.join(os.getcwd(), "downloads")
                os.makedirs(download_folder, exist_ok=True)  # Ensure download folder exists
                
                # Explicitly wait a moment before clicking to ensure all elements are loaded
                await page.wait_for_timeout(1000)  # Wait 1 second before clicking

                # Use context manager to wait for the download event
                async with page.expect_download(timeout=120000) as download_info:  # Timeout set to 120 seconds
                    await download_button.click()  # Trigger the download by clicking the button
                    print("Download button clicked, waiting for download...")

                    # Await the download object to access the file path
                    downloaded_file = await download_info.value
                    downloaded_file_path = await downloaded_file.path()  # Get the file path of the downloaded file

                    print(f"File downloaded to: {downloaded_file_path}")

                # Define the path where to save the file
                saved_path = os.path.join(download_folder, "transcript.pdf")
                
                # Save the downloaded file locally by moving it
                os.rename(downloaded_file_path, saved_path)
                print(f"File saved to {saved_path}")
            else:
                print("Download button not found!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Close browser
            await browser.close()

# Run the scraping function asynchronously
asyncio.run(scrape_transcripts())
