from playwright.sync_api import Page

from tests.utils.allure_helper import goto_with_allure


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.add_spending_button_link = page.get_by_role("link", name="New spending")
        Page.goto = goto_with_allure
