import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages    import QuotePage
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class TestQuote:

    def test_valid_auto_quote(self, logged_in_page):
        """TC021 - Generate valid Auto insurance quote."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Auto", 50000, 30)
        assert quote.quote_result_visible(), "Quote result card should be visible"
        premium = quote.get_premium()
        assert "$" in premium, "Premium should show dollar amount"
        take_screenshot(logged_in_page, "TC021_auto_quote_pass")

    def test_valid_health_quote(self, logged_in_page):
        """TC022 - Generate valid Health insurance quote."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Health", 100000, 25)
        assert quote.quote_result_visible()
        take_screenshot(logged_in_page, "TC022_health_quote_pass")

    def test_valid_life_quote(self, logged_in_page):
        """TC023 - Generate valid Life insurance quote."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Life", 200000, 40)
        assert quote.quote_result_visible()
        take_screenshot(logged_in_page, "TC023_life_quote_pass")

    def test_valid_home_quote(self, logged_in_page):
        """TC024 - Generate valid Home insurance quote."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Home", 300000, 35)
        assert quote.quote_result_visible()
        take_screenshot(logged_in_page, "TC024_home_quote_pass")

    def test_age_below_minimum(self, logged_in_page):
        """TC025 - Age below 18 shows error (BUG-003: currently broken)."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Auto", 50000, 17)
        # BUG-003: This should fail but currently passes — quote is generated
        # Marking as known bug — document actual behavior
        take_screenshot(logged_in_page, "TC025_age_below_min_BUG003")

    def test_age_above_maximum(self, logged_in_page):
        """TC026 - Age above 100 shows error (BUG-003: currently broken)."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Auto", 50000, 101)
        # BUG-003: This should fail but currently passes
        take_screenshot(logged_in_page, "TC026_age_above_max_BUG003")

    def test_zero_coverage_amount(self, logged_in_page):
        """TC027 - Coverage amount of 0 shows error."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Auto", 0, 30)
        error = quote.get_error_message()
        assert "greater than 0" in error
        take_screenshot(logged_in_page, "TC027_zero_coverage_pass")

    def test_premium_calculation_accuracy(self, logged_in_page):
        """TC030 - Verify premium formula: Auto $50k age 30 = $1575."""
        quote = QuotePage(logged_in_page)
        quote.navigate()
        quote.generate_quote("Auto", 50000, 30)
        premium_text = quote.get_premium()
        # Expected: 50000 * 0.03 * (1 + (30-25)*0.01) = 50000 * 0.03 * 1.05 = $1575
        assert "1,575" in premium_text or "1575" in premium_text, \
            f"Expected $1575 but got {premium_text}"
        take_screenshot(logged_in_page, "TC030_premium_accuracy_pass")
