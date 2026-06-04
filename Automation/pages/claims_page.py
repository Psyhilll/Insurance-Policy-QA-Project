from locators import ClaimsLocators, ClaimTrackingLocators
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class ClaimsPage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/claims"

    def navigate(self):
        self.page.goto(self.url)

    def submit_claim(self, policy_index, amount, reason):
        """policy_index: index of option in the select dropdown (1-based)"""
        self.page.locator(ClaimsLocators.POLICY_SELECT).select_option(index=policy_index)
        self.page.fill(ClaimsLocators.CLAIM_AMOUNT, str(amount))
        self.page.fill(ClaimsLocators.CLAIM_REASON, reason)
        self.page.click(ClaimsLocators.SUBMIT_BUTTON)

    def get_error_message(self):
        self.page.wait_for_selector(ClaimsLocators.ERROR_ALERT, timeout=3000)
        return self.page.text_content(ClaimsLocators.ERROR_ALERT).strip()

    def get_success_message(self):
        self.page.wait_for_selector(ClaimsLocators.SUCCESS_ALERT, timeout=3000)
        return self.page.text_content(ClaimsLocators.SUCCESS_ALERT).strip()

    def has_no_policies(self):
        return self.page.is_visible(ClaimsLocators.NO_POLICY_MSG)

    def screenshot(self, name="claims"):
        take_screenshot(self.page, name)


class ClaimTrackingPage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/claim-tracking"

    def navigate(self):
        self.page.goto(self.url)

    def get_claim_count(self):
        rows = self.page.locator(ClaimTrackingLocators.CLAIM_ROWS)
        return rows.count()

    def get_latest_claim_status(self):
        badges = self.page.locator(ClaimTrackingLocators.STATUS_BADGES)
        return badges.first.text_content().strip()

    def screenshot(self, name="claim_tracking"):
        take_screenshot(self.page, name)
