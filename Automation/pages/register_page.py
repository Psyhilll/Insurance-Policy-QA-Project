from locators import RegisterLocators
from utilities import take_screenshot

BASE_URL = "http://localhost:5000"


class RegisterPage:
    def __init__(self, page):
        self.page = page
        self.url  = f"{BASE_URL}/register"

    def navigate(self):
        self.page.goto(self.url)

    def register(self, first_name, last_name, email,
                 password, confirm_password, phone="", dob=""):
        self.page.fill(RegisterLocators.FIRST_NAME,    first_name)
        self.page.fill(RegisterLocators.LAST_NAME,     last_name)
        self.page.fill(RegisterLocators.EMAIL,         email)
        if phone:
            self.page.fill(RegisterLocators.PHONE, phone)
        if dob:
            self.page.fill(RegisterLocators.DATE_OF_BIRTH, dob)
        self.page.fill(RegisterLocators.PASSWORD,      password)
        self.page.fill(RegisterLocators.CONFIRM_PASS,  confirm_password)
        self.page.click(RegisterLocators.SUBMIT_BUTTON)

    def get_error_message(self):
        self.page.wait_for_selector(RegisterLocators.ERROR_ALERT, timeout=3000)
        return self.page.text_content(RegisterLocators.ERROR_ALERT).strip()

    def get_success_message(self):
        self.page.wait_for_selector(RegisterLocators.SUCCESS_ALERT, timeout=3000)
        return self.page.text_content(RegisterLocators.SUCCESS_ALERT).strip()

    def is_on_login_page(self):
        return "/login" in self.page.url

    def screenshot(self, name="register"):
        take_screenshot(self.page, name)
