from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()

    page.goto("https://example.com/dashboard")  # or any page after login

    # You are now logged in!
    print(page.title())
    browser.close()
