from .base_page import BasePage
import allure


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Type your username")
        self.password_input = page.get_by_placeholder("Type your password")
        self.login_button = page.get_by_role("button", name="Log in")
        self.signin_invalid_creds_error = page.locator("p.form__error")

    @allure.step("Авторизуемся")
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
