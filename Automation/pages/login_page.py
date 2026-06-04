from locators import LoginLocators
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/login"

    def navigate(self):
        self.page.goto(self.url)

    def login(self, email, password):
        self.page.fill(LoginLocators.EMAIL_INPUT,    email)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        self.page.click(LoginLocators.SUBMIT_BUTTON)

    def get_error_message(self):
        self.page.wait_for_selector(LoginLocators.ERROR_ALERT, timeout=3000)
        return self.page.text_content(LoginLocators.ERROR_ALERT).strip()

    def is_on_dashboard(self):
        return "/dashboard" in self.page.url

    def is_on_admin(self):
        return "/admin" in self.page.url

    def screenshot(self, name="login"):
        take_screenshot(self.page, name)
