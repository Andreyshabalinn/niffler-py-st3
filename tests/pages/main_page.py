from .base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.success_add_spending_popup = page.get_by_text(
            "New spending is successfully created"
        )
