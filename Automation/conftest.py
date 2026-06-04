import pytest
from playwright.sync_api import sync_playwright

# ── Base URL ──────────────────────────────────────────────────────────────────
BASE_URL = "http://localhost:5000"

# ── Test Users ────────────────────────────────────────────────────────────────
ADMIN_EMAIL    = "admin@insurance.com"
ADMIN_PASSWORD = "Admin@1234"
TEST_EMAIL     = "playwright@test.com"
TEST_PASSWORD  = "Test@1234"
TEST_FIRSTNAME = "Playwright"
TEST_LASTNAME  = "Tester"


@pytest.fixture(scope="session")
def browser_instance():
    """Launch browser once for the whole test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    """Fresh browser context and page for each test."""
    context = browser_instance.new_context(viewport={"width": 1280, "height": 720})
    page    = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """Page already logged in as test customer."""
    page.goto(f"{BASE_URL}/login")
    page.fill("#email",    TEST_EMAIL)
    page.fill("#password", TEST_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_url(f"{BASE_URL}/dashboard")
    yield page


@pytest.fixture(scope="function")
def admin_page(page):
    """Page already logged in as admin."""
    page.goto(f"{BASE_URL}/login")
    page.fill("#email",    ADMIN_EMAIL)
    page.fill("#password", ADMIN_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_url(f"{BASE_URL}/admin")
    yield page
