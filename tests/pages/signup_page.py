from .base_page import BasePage
from .login_page import LoginPage

class SignupPage(LoginPage):
    def __init__(self, page):
        super().__init__(page)
        self.password_submit_input = page.get_by_placeholder("Submit your password")
        self.signup_button = page.get_by_role("button", name="Sign up")
        self.signin_button_link = page.get_by_role("link", name="Sign in")

    def signup(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.password_submit_input.fill(password)
        self.signup_button.click()
        self.signin_button_link.wait_for()
        self.signin_button_link.click()