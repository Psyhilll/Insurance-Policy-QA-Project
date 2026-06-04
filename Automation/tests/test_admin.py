import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages    import AdminPage, LoginPage
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class TestAdmin:

    def test_admin_dashboard_loads(self, admin_page):
        """TC051 - Admin dashboard loads with stat cards."""
        admin = AdminPage(admin_page)
        assert admin.is_on_admin_page(), "Should be on admin dashboard"
        # Verify stat cards are present
        cards = admin_page.locator(".stat-card")
        assert cards.count() >= 4, "Should have at least 4 stat cards"
        take_screenshot(admin_page, "TC051_admin_dashboard_pass")

    def test_admin_can_view_customers(self, admin_page):
        """TC052 - Admin can view customer list."""
        admin = AdminPage(admin_page)
        admin.go_to_customers()
        assert "/admin/customers" in admin_page.url
        # Table should be visible
        assert admin_page.is_visible("table")
        take_screenshot(admin_page, "TC052_admin_customers_pass")

    def test_admin_can_view_claims(self, admin_page):
        """TC053 - Admin can view all claims."""
        admin = AdminPage(admin_page)
        admin.go_to_claims()
        assert "/admin/claims" in admin_page.url
        take_screenshot(admin_page, "TC053_admin_claims_pass")

    def test_non_admin_cannot_access_admin_panel(self, page):
        """TC058 - BUG-002: Customer should NOT access /admin directly.
        Currently FAILING due to BUG-002 (missing @admin_required decorator)."""
        login = LoginPage(page)
        login.navigate()
        login.login("playwright@test.com", "Test@1234")
        page.wait_for_url(f"{BASE_URL}/dashboard")

        # Try to access admin directly
        page.goto(f"{BASE_URL}/admin")

        # BUG-002: This assertion FAILS because admin loads for non-admin users
        assert "/login" in page.url or "Admin access required" in page.content(), \
            "BUG-002: Non-admin customer can access /admin — security vulnerability!"
        take_screenshot(page, "TC058_admin_access_BUG002_FAIL")

    def test_admin_approve_claim(self, admin_page):
        """TC054 - Admin can approve a pending claim."""
        admin = AdminPage(admin_page)
        admin.go_to_claims()

        approve_btn = admin_page.locator("button[value='Approved']").first
        if approve_btn.count() == 0:
            pytest.skip("No pending claims to approve")

        approve_btn.click()
        # Should reload and show success
        assert "/admin/claims" in admin_page.url
        take_screenshot(admin_page, "TC054_admin_approve_claim_pass")

    def test_admin_reject_claim(self, admin_page):
        """TC055 - Admin can reject a pending claim."""
        admin = AdminPage(admin_page)
        admin.go_to_claims()

        reject_btn = admin_page.locator("button[value='Rejected']").first
        if reject_btn.count() == 0:
            pytest.skip("No pending claims to reject")

        reject_btn.click()
        assert "/admin/claims" in admin_page.url
        take_screenshot(admin_page, "TC055_admin_reject_claim_pass")
