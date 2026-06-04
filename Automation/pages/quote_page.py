from locators import QuoteLocators
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class QuotePage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/quote"

    def navigate(self):
        self.page.goto(self.url)

    def generate_quote(self, policy_type, coverage_amount, age):
        self.page.select_option(QuoteLocators.POLICY_TYPE,     policy_type)
        self.page.fill(QuoteLocators.COVERAGE_AMOUNT, str(coverage_amount))
        self.page.fill(QuoteLocators.AGE,             str(age))
        self.page.click(QuoteLocators.SUBMIT_BUTTON)

    def get_premium(self):
        self.page.wait_for_selector(QuoteLocators.RESULT_CARD, timeout=4000)
        return self.page.text_content(QuoteLocators.PREMIUM_DISPLAY).strip()

    def quote_result_visible(self):
        return self.page.is_visible(QuoteLocators.RESULT_CARD)

    def click_purchase(self):
        self.page.click(QuoteLocators.PURCHASE_BUTTON)

    def get_error_message(self):
        self.page.wait_for_selector(QuoteLocators.ERROR_ALERT, timeout=3000)
        return self.page.text_content(QuoteLocators.ERROR_ALERT).strip()

    def screenshot(self, name="quote"):
        take_screenshot(self.page, name)
