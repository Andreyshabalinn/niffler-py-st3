import allure
from .main_page import MainPage
from playwright.sync_api import Locator
from tests.config import BASE_URL

base_url = BASE_URL


class SpendingsPage(MainPage):
    def __init__(self, page):
        super().__init__(page)
        self.amount_input = page.locator("#amount")
        self.currency_combobox = page.locator("#currency")
        self.category_input = page.locator("#category")
        self.date_calendar = page.get_by_label("Date")
        self.description_input = page.locator("#description")
        self.add_spending_button = page.get_by_role("button", name="Add")
        self.delete_spending_button = page.locator("#delete")
        self.delete_spending_dialog = page.get_by_role("dialog")
        self.delete_spending_dialog_button = self.delete_spending_dialog.get_by_role(
            "button", name="Delete"
        )
        self.delete_spending_popup = page.get_by_text("Spendings succesfully deleted")
        self.select_all_rows_checkbox = page.get_by_role(
            "checkbox", name="select all rows"
        )
        self.no_spendings_text = page.locator(
            "p.MuiTypography-h6", has_text="There are no spendings"
        )
        self.edit_spending_header = page.get_by_role("heading", name="Edit spending")
        self.save_editing_spending_button = page.get_by_role(
            "button", name="Save changes"
        )
        self.edit_spending_success_popup = page.get_by_text(
            "Spending is edited successfully"
        )
        self.spending_search_input = page.get_by_placeholder("Search")
        self.spending_currency_filter = page.locator("#currency")
        self.spending_amount_error = page.locator(
            "span", has_text="Amount has to be not less then 0.01"
        )

    @allure.step("Ищем ряд определённой траты")
    def spending_row(
        self, spending_category: str, spending_amount: str, spending_date: str
    ) -> Locator:
        return self.page.locator(
            f'tr:has(span:has-text("{spending_category}")):has(span:has-text("{spending_amount}")):has(span:has-text("{spending_date}"))'
        )

    @allure.step("Создаём трату")
    def add_spending(
        self,
        spending_amount: str,
        spending_currency: str,
        spending_category: str,
        spending_date: str,
        spending_description: str,
    ):
        self.add_spending_button_link.click()
        self.page.wait_for_url(f"{base_url}spending")
        self.amount_input.fill(spending_amount)

        # Открываем выпадающий список (по combobox)
        self.currency_combobox.click()

        # Выбираем нужный пункт
        self.page.get_by_role("option", name=spending_currency).click()

        self.category_input.fill(spending_category)

        # Открыть календарь
        self.date_calendar.click()

        # Ждём, пока он появится
        self.page.locator(".MuiDateCalendar-root").wait_for()

        # Кликаем по нужному дню
        self.page.get_by_role("gridcell", name=spending_date, exact=True).click()
        self.description_input.fill(spending_description)

        self.add_spending_button.click()

        self.success_add_spending_popup.wait_for()

    @allure.step("Редактируем трату")
    def edit_spending(
        self,
        spending_category: str,
        spending_date: str,
        spending_description: str,
        new_spending_amount: str,
        new_spending_currency: str,
        new_spending_category: str,
        new_spending_date: str,
        new_spending_description: str,
    ):
        row = (
            self.page.locator("tr")
            .filter(has=self.page.locator(f'span:has-text("{spending_category}")'))
            .filter(has=self.page.locator(f'span:has-text("{spending_description}")'))
            .filter(has=self.page.locator(f'span:has-text("{spending_date}")'))
        )

        row.locator('button[aria-label="Edit spending"]').click()
        self.edit_spending_header.wait_for()
        self.amount_input.fill(new_spending_amount)

        # Открываем выпадающий список (по combobox)
        self.currency_combobox.click()

        # Выбираем нужный пункт
        self.page.get_by_role("option", name=new_spending_currency).click()

        self.category_input.fill(new_spending_category)

        # Открыть календарь
        self.date_calendar.click()

        # Ждём, пока он появится
        self.page.locator(".MuiDateCalendar-root").wait_for()

        # Кликаем по нужному дню
        self.page.get_by_role("gridcell", name=new_spending_date, exact=True).click()

        self.description_input.fill(new_spending_description)

        self.save_editing_spending_button.click()

        self.edit_spending_success_popup.wait_for()

        row = self.page.locator(
            f'tr:has(span:has-text("{new_spending_category}")):has(span:has-text("{new_spending_amount}"))'
        )
        row.wait_for()

    @allure.step("Редактируем трату невалидными значениями")
    def edit_invalid_spending(
        self,
        spending_category: str,
        spending_date: str,
        spending_description: str,
        new_spending_amount: str,
    ):
        row = (
            self.page.locator("tr")
            .filter(has=self.page.locator(f'span:has-text("{spending_category}")'))
            .filter(has=self.page.locator(f'span:has-text("{spending_description}")'))
            .filter(has=self.page.locator(f'span:has-text("{spending_date}")'))
        )

        row.locator('button[aria-label="Edit spending"]').click()
        self.edit_spending_header.wait_for()
        self.amount_input.fill(new_spending_amount)
        self.amount_input.press("Enter")

    @allure.step("Удаляем трату")
    def delete_spending(self, category_name: str, spend_amount: str, spend_date: str):
        row = self.page.locator(
            f'tr:has(span:has-text("{category_name}")):has(span:has-text("{spend_amount}")):has(span:has-text("{spend_date}"))'
        )
        row.click()
        self.delete_spending_button.click()
        self.delete_spending_dialog.wait_for()
        self.delete_spending_dialog_button.click()

        self.delete_spending_popup.wait_for()

        return row

    @allure.step("Удаляем все траты")
    def delete_all_spending(self):
        self.select_all_rows_checkbox.click()
        self.delete_spending_button.click()
        self.delete_spending_dialog.wait_for()
        self.delete_spending_dialog_button.click()

        self.no_spendings_text.wait_for()
        self.delete_spending_popup.wait_for()

    @allure.step("Ищем трату по её категории")
    def search_spending_by_category(self, category_name: str):
        self.spending_search_input.fill(category_name)
        self.spending_search_input.press("Enter")

    @allure.step("Ищем трату по её валюте")
    def search_spending_by_currency(self, spending_currency: str):
        self.spending_currency_filter.click()
        self.page.locator(f'[data-value="{spending_currency}"]').click()
