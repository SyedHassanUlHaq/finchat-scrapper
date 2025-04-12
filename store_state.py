from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False for manual login
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com/login")

    input("Login manually and press Enter here once done...")

    # Save cookies
    storage = context.storage_state(path="auth.json")

    browser.close()
