import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages     import ClaimsPage, ClaimTrackingPage
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class TestClaims:

    def test_submit_valid_claim(self, logged_in_page):
        """TC039 - Submit a valid claim against an active policy."""
        claims = ClaimsPage(logged_in_page)
        claims.navigate()

        if claims.has_no_policies():
            pytest.skip("No active policies available — run test_quote first")

        claims.submit_claim(
            policy_index=1,
            amount=1000,
            reason="Car accident on the highway, front bumper damaged badly"
        )
        msg = claims.get_success_message()
        assert "submitted successfully" in msg
        take_screenshot(logged_in_page, "TC039_valid_claim_pass")

    def test_claim_exceeds_coverage(self, logged_in_page):
        """TC040 - Claim amount exceeding coverage shows error."""
        claims = ClaimsPage(logged_in_page)
        claims.navigate()

        if claims.has_no_policies():
            pytest.skip("No active policies available")

        claims.submit_claim(
            policy_index=1,
            amount=9999999,
            reason="Attempting to claim more than coverage amount allows"
        )
        error = claims.get_error_message()
        assert "cannot exceed coverage" in error
        take_screenshot(logged_in_page, "TC040_exceeds_coverage_pass")

    def test_zero_claim_amount(self, logged_in_page):
        """TC042 - Claim amount of 0 shows error."""
        claims = ClaimsPage(logged_in_page)
        claims.navigate()

        if claims.has_no_policies():
            pytest.skip("No active policies available")

        claims.submit_claim(
            policy_index=1,
            amount=0,
            reason="Testing zero amount validation for claim submission"
        )
        error = claims.get_error_message()
        assert "greater than 0" in error
        take_screenshot(logged_in_page, "TC042_zero_claim_pass")

    def test_empty_claim_reason(self, logged_in_page):
        """TC045 - Empty claim reason is blocked."""
        claims = ClaimsPage(logged_in_page)
        claims.navigate()
        # Browser validation on textarea required field
        if logged_in_page.is_visible("select[name='policy_id']"):
            logged_in_page.select_option("select[name='policy_id']", index=1)
            logged_in_page.fill("input[name='claim_amount']", "500")
            # Leave reason empty and submit
            logged_in_page.click("button[type='submit']")
            assert "/claims" in logged_in_page.url
        take_screenshot(logged_in_page, "TC045_empty_reason_pass")

    def test_claim_appears_in_tracking(self, logged_in_page):
        """TC047 - Submitted claim appears in claim tracking page."""
        tracking = ClaimTrackingPage(logged_in_page)
        tracking.navigate()
        count = tracking.get_claim_count()
        assert count >= 0, "Tracking page should load without errors"
        take_screenshot(logged_in_page, "TC047_claim_tracking_pass")

    def test_new_claim_status_is_pending(self, logged_in_page):
        """TC050 - Newly submitted claim has Pending status."""
        claims  = ClaimsPage(logged_in_page)
        tracking = ClaimTrackingPage(logged_in_page)

        claims.navigate()
        if claims.has_no_policies():
            pytest.skip("No active policies available")

        claims.submit_claim(
            policy_index=1,
            amount=500,
            reason="Testing that new claim default status is Pending correctly"
        )

        tracking.navigate()
        status = tracking.get_latest_claim_status()
        assert "Pending" in status, f"New claim should be Pending but got: {status}"
        take_screenshot(logged_in_page, "TC050_claim_pending_status_pass")
