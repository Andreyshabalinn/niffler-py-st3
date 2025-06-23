import time
from playwright.sync_api import Page
from faker import Faker
from datetime import date, datetime, timezone
from pages.spendings_page import SpendingsPage
from pages.profile_page import ProfilePage
from api_controller import create_spending
fake = Faker()
from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv("BASE_URL")

def load():
    pass

# #Создание траты
def test_create_spend(page: Page, signin_user):

    spending_amount = str(fake.random_int(min=10, max=10000))
    spending_currency = "KZT"
    spending_category = fake.word()
    today = date.today()
    spending_date = str(today.day)
    spending_description = fake.word()
    
    spendings_page = SpendingsPage(page)  

    spendings_page.add_spending(spending_amount, spending_currency, spending_category, spending_date, spending_description)

    row = page.locator(
    f'tr:has(span:has-text("{spending_category}")):has(span:has-text("{spending_amount}")):has(span:has-text("{spending_date}"))')
    row.wait_for()


    spendings_page.delete_spending(spending_category, spending_amount, spending_date)

    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.archive_category(spending_category)


def test_create_invalid_spend(page: Page, signin_user):
    spending_amount = "0"
    spendings_page = SpendingsPage(page)
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

    spending_page = SpendingsPage(page)
    row = spending_page.delete_spending(category_name, spend_amount, spend_date)
    assert row.is_hidden()

    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.archive_category(category_name)


