from playwright.sync_api import sync_playwright

chrome_path = "/usr/bin/google-chrome"  # or "google-chrome-stable", use `which google-chrome` to verify
user_data_dir = "/home/syed-hassan-ul-haq/.config/google-chrome"  # full directory, not just Default

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        executable_path=chrome_path,
        args=["--profile-directory=Default"]
    )

    page = browser.pages[0]
    page.goto("https://finchat.io/company/NasdaqGS-AAPL/investor-relations/Q1-2025/")

    input("If you're logged in, press Enter to close.")
    browser.close()
 