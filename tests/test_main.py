import time
from playwright.sync_api import Page
from faker import Faker
from datetime import date, datetime, timezone
from pages.spendings_page import SpendingsPage
from api_controller import create_spending
fake = Faker()

#Создание траты
def test_create_spend(page: Page, signin_user):

    spending_amount = str(fake.random_int(min=10, max=10000))
    spending_currency = "KZT"
    spending_category = fake.word()
    today = date.today()
    spending_date = str(today.day)
    spending_description = fake.word()
    
    spendings_page = SpendingsPage(page)

    page.goto("http://frontend.niffler.dc/main")    

    spendings_page.add_spending(spending_amount, spending_currency, spending_category, spending_date, spending_description)

    row = page.locator(
    f'tr:has(span:has-text("{spending_category}")):has(span:has-text("{spending_amount}")):has(span:has-text("{spending_date}"))')

    assert row.is_visible()


def test_create_invalid_spend(page: Page, signin_user):
    spending_amount = "0"
    spendings_page = SpendingsPage(page)
    page.goto("http://frontend.niffler.dc/main")
    spendings_page.add_spending_button_link.click()

    spendings_page.amount_input.fill(spending_amount)
    spendings_page.amount_input.press("Enter")

    assert page.locator("span", has_text="Amount has to be not less then 0.01").is_visible()


def test_delete_spend(page: Page, signin_user):
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word()
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    today = date.today()
    spend_date = str(today.day)
    page.reload()
    time.sleep(2)
    row = page.locator(
    f'tr:has(span:has-text("{category_name}")):has(span:has-text("{spend_amount}")):has(span:has-text("{spend_date}"))')
    assert row.is_visible()
    row.click()
    page.locator("#delete").click()
    dialog = page.get_by_role("dialog")
    dialog.wait_for()
    dialog.get_by_role("button", name="Delete").click()
    page.get_by_text(f"Spendings succesfully deleted").wait_for()
    assert row.is_hidden()


    




#Редактирование траты

#Удаление траты

#Поиск траты


