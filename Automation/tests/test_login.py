import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages    import LoginPage
from utilities import take_screenshot

BASE_URL     = "http://localhost:5000"
VALID_EMAIL  = "playwright@test.com"
VALID_PASS   = "Test@1234"
ADMIN_EMAIL  = "admin@insurance.com"
ADMIN_PASS   = "Admin@1234"


class TestLogin:

    def test_valid_customer_login(self, page):
        """TC011 - Login with valid customer credentials."""
        login = LoginPage(page)
        login.navigate()
        login.login(VALID_EMAIL, VALID_PASS)
        page.wait_for_url(f"{BASE_URL}/dashboard", timeout=5000)
        assert "/dashboard" in page.url, "Should redirect to dashboard after login"
        take_screenshot(page, "TC011_valid_login_pass")

    def test_invalid_password(self, page):
        """TC012 - Login with wrong password shows error."""
        login = LoginPage(page)
        login.navigate()
        login.login(VALID_EMAIL, "WrongPassword999")
        error = login.get_error_message()
        assert "Invalid email or password" in error
        take_screenshot(page, "TC012_invalid_password_pass")

    def test_nonexistent_email(self, page):
        """TC013 - Login with unregistered email shows error."""
        login = LoginPage(page)
        login.navigate()
        login.login("nobody@nowhere.com", "Test@1234")
        error = login.get_error_message()
        assert "Invalid email or password" in error
        take_screenshot(page, "TC013_nonexistent_email_pass")

    def test_empty_email(self, page):
        """TC014 - Login with blank email blocked by browser validation."""
        login = LoginPage(page)
        login.navigate()
        page.fill("#password", "Test@1234")
        page.click("button[type='submit']")
        # Browser prevents submission — still on login page
        assert "/login" in page.url
        take_screenshot(page, "TC014_empty_email_pass")

    def test_empty_password(self, page):
        """TC015 - Login with blank password blocked by browser validation."""
        login = LoginPage(page)
        login.navigate()
        page.fill("#email", VALID_EMAIL)
        page.click("button[type='submit']")
        assert "/login" in page.url
        take_screenshot(page, "TC015_empty_password_pass")

    def test_admin_login(self, page):
        """TC016 - Admin login redirects to admin dashboard."""
        login = LoginPage(page)
        login.navigate()
        login.login(ADMIN_EMAIL, ADMIN_PASS)
        page.wait_for_url(f"{BASE_URL}/admin", timeout=5000)
        assert "/admin" in page.url, "Admin should land on /admin dashboard"
        take_screenshot(page, "TC016_admin_login_pass")

    def test_logout_clears_session(self, page):
        """TC018 - Logout ends session, accessing dashboard redirects to login."""
        login = LoginPage(page)
        login.navigate()
        login.login(VALID_EMAIL, VALID_PASS)
        page.wait_for_url(f"{BASE_URL}/dashboard")
        page.goto(f"{BASE_URL}/logout")
        page.goto(f"{BASE_URL}/dashboard")
        assert "/login" in page.url, "After logout, dashboard should redirect to login"
        take_screenshot(page, "TC018_logout_pass")

    def test_direct_dashboard_access_without_login(self, page):
        """TC019 - Accessing dashboard without login redirects to login page."""
        page.goto(f"{BASE_URL}/dashboard")
        assert "/login" in page.url, "Unauthenticated user should be redirected"
        take_screenshot(page, "TC019_auth_redirect_pass")
