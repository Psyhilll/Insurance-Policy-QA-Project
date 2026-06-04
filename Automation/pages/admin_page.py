from locators import AdminLocators
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class AdminPage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/admin"

    def navigate(self):
        self.page.goto(self.url)

    def go_to_claims(self):
        self.page.goto(f"{BASE_URL}/admin/claims")

    def go_to_customers(self):
        self.page.goto(f"{BASE_URL}/admin/customers")

    def approve_first_pending_claim(self):
        self.page.click(AdminLocators.APPROVE_BUTTON)

    def reject_first_pending_claim(self):
        self.page.click(AdminLocators.REJECT_BUTTON)

    def get_stat_values(self):
        cards = self.page.locator(AdminLocators.STAT_CARDS)
        return [cards.nth(i).text_content().strip() for i in range(cards.count())]

    def is_on_admin_page(self):
        return "/admin" in self.page.url

    def screenshot(self, name="admin"):
        take_screenshot(self.page, name)
