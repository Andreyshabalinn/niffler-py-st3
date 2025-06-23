from .login_page import LoginPage
from playwright.sync_api import Locator

class SignupPage(LoginPage):
    def __init__(self, page):
        super().__init__(page)
        self.password_submit_input = page.get_by_placeholder("Submit your password")
        self.signup_button = page.get_by_role("button", name="Sign up")
        self.signin_button_link = page.get_by_role("link", name="Sign in")
        self.signup_username_len_error = page.locator("span.form__error", has_text=f"Allowed username length should be from 3 to 50 characters")
        self.signup_unmatched_passwords_error = page.locator("span.form__error", has_text=f"Passwords should be equal")
        self.signup_password_len_error = page.locator("span.form__error", has_text=f"Allowed password length should be from 3 to 12 characters").first

    
    def user_already_exists_span(self, username:str)->Locator:
        return self.page.locator("span.form__error", has_text=f"Username `{username}` already exists")

        


    def signup(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.password_submit_input.fill(password)
        self.signup_button.click()
        if self.signup_username_len_error.is_hidden() and self.signup_password_len_error.is_hidden():
            if self.signin_button_link.is_visible():
                self.signin_button_link.click()


    def signup_with_unmatched_passwords(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.password_submit_input.fill(password+"Test")
        self.signup_button.click()
        self.signup_unmatched_passwords_error.wait_for()
