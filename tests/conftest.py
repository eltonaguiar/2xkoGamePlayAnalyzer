"""
Pytest configuration for Playwright tests.
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import os

PORT = 8002
BASE_URL = f"http://localhost:{PORT}"


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for all tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser):
    """Create a new page for each test"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
        record_video_dir=None,  # Disable video recording for speed
    )
    page = context.new_page()
    
    # Capture console errors
    console_messages = []
    
    def handle_console(msg):
        console_messages.append(msg)
    
    page.on("console", handle_console)
    
    yield page
    
    # Print console errors if any
    errors = [msg for msg in console_messages if msg.type == "error"]
    if errors:
        print(f"\nConsole errors in test:")
        for error in errors:
            print(f"  - {error.text}")
    
    context.close()


@pytest.fixture
def loaded_database_page(page: Page):
    """Fixture that loads the database page and waits for it to be ready"""
    try:
        page.goto(f"{BASE_URL}/character_database.html", wait_until="networkidle", timeout=15000)
    except Exception:
        # Fallback if networkidle times out
        page.goto(f"{BASE_URL}/character_database.html", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_load_state("networkidle", timeout=10000)
    # Wait for initial data load
    page.wait_for_selector("header", timeout=5000)
    return page


@pytest.fixture
def loaded_embedded_page(page: Page):
    """Fixture that loads the embedded page and waits for it to be ready"""
    try:
        page.goto(f"{BASE_URL}/character_database_embedded.html", wait_until="networkidle", timeout=15000)
    except Exception:
        # Fallback if networkidle times out
        page.goto(f"{BASE_URL}/character_database_embedded.html", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_load_state("networkidle", timeout=10000)
    page.wait_for_selector("header", timeout=5000)
    return page


@pytest.fixture
def moves_tab_ready(loaded_database_page: Page):
    """Fixture that ensures Move Database tab is active and ready"""
    page = loaded_database_page
    # Wait for page to be ready
    page.wait_for_load_state("networkidle", timeout=10000)
    # Click the Move Comparison tab (actual tab name in HTML)
    page.click("text=Move Comparison", timeout=5000)
    page.wait_for_selector("#moves-container", state="visible", timeout=10000)
    return page
