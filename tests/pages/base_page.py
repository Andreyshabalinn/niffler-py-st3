from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.add_spending_button_link = page.get_by_role("link", name="New spending")