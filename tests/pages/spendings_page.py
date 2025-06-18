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

    def add_spending(self, spending_amount, spending_currency, spending_category, spending_date, spending_description):

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