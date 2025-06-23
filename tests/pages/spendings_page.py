from .main_page import MainPage

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
        self.delete_spending_dialog_button = self.delete_spending_dialog.get_by_role("button", name="Delete")
        self.delete_spending_popup = page.get_by_text(f"Spendings succesfully deleted")
        

    def add_spending(self, spending_amount: str, spending_currency: str, spending_category: str, spending_date: str, spending_description: str):

        self.add_spending_button_link.click()
        self.page.wait_for_url("http://frontend.niffler.dc/spending")
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
        self.page.get_by_role("gridcell", name=spending_date).click()


        self.description_input.fill(spending_description)

        self.add_spending_button.click()

        self.success_add_spending_popup.wait_for()


    def delete_spending(self, category_name: str, spend_amount: str, spend_date: str):
        row = self.page.locator(
        f'tr:has(span:has-text("{category_name}")):has(span:has-text("{spend_amount}")):has(span:has-text("{spend_date}"))')
        row.click()
        self.delete_spending_button.click()
        self.delete_spending_dialog.wait_for()
        self.delete_spending_dialog_button.click()

        self.delete_spending_popup.wait_for()
        
        return row
    

