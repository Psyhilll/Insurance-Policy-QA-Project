import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages     import RegisterPage, LoginPage
from utilities import random_email, take_screenshot

BASE_URL = "http://localhost:5000"


class TestRegistration:

    def test_valid_registration(self, page):
        """TC001 - Register with all valid details."""
        reg   = RegisterPage(page)
        email = random_email()
        reg.navigate()
        reg.register(
            first_name="Playwright",
            last_name="Tester",
            email=email,
            password="Test@1234",
            confirm_password="Test@1234",
            phone="204-555-9999"
        )
        msg = reg.get_success_message()
        assert "Account created successfully" in msg
        assert reg.is_on_login_page()
        take_screenshot(page, "TC001_valid_registration_pass")

    def test_duplicate_email(self, page):
        """TC002 - Register with already-used email shows error."""
        reg = RegisterPage(page)
        reg.navigate()
        reg.register(
            first_name="John",
            last_name="Doe",
            email="playwright@test.com",   # already registered
            password="Test@1234",
            confirm_password="Test@1234"
        )
        error = reg.get_error_message()
        assert "Email already registered" in error
        take_screenshot(page, "TC002_duplicate_email_pass")

    def test_password_mismatch(self, page):
        """TC004 - Mismatched passwords show error."""
        reg = RegisterPage(page)
        reg.navigate()
        reg.register(
            first_name="John",
            last_name="Doe",
            email=random_email(),
            password="Test@1234",
            confirm_password="Different@9999"
        )
        error = reg.get_error_message()
        assert "Passwords do not match" in error
        take_screenshot(page, "TC004_password_mismatch_pass")

    def test_short_password(self, page):
        """TC005 - Password under 8 characters shows error."""
        reg = RegisterPage(page)
        reg.navigate()
        reg.register(
            first_name="John",
            last_name="Doe",
            email=random_email(),
            password="abc",
            confirm_password="abc"
        )
        error = reg.get_error_message()
        assert "at least 8 characters" in error
        take_screenshot(page, "TC005_short_password_pass")

    def test_empty_required_fields(self, page):
        """TC003 - Submitting empty form is blocked."""
        reg = RegisterPage(page)
        reg.navigate()
        page.click("button[type='submit']")
        # Browser validation prevents submission
        assert "/register" in page.url
        take_screenshot(page, "TC003_empty_fields_pass")

    def test_registration_then_login(self, page):
        """End-to-end: Register → Login → Reach Dashboard."""
        email = random_email()
        # Register
        reg = RegisterPage(page)
        reg.navigate()
        reg.register("E2E", "User", email, "Test@1234", "Test@1234")
        assert "Account created successfully" in reg.get_success_message()
        # Login
        login = LoginPage(page)
        login.login(email, "Test@1234")
        page.wait_for_url(f"{BASE_URL}/dashboard", timeout=5000)
        assert "/dashboard" in page.url
        take_screenshot(page, "E2E_register_to_dashboard_pass")
