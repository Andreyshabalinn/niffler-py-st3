import time
from playwright.sync_api import Page
from faker import Faker
from datetime import date, datetime, timedelta, timezone
from pages.spendings_page import SpendingsPage
from pages.profile_page import ProfilePage
from api_controller import create_spending, delete_spending
fake = Faker()
from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv("BASE_URL")

def test_create_spend(page: Page, signin_user):
    # Входные данные для создаваемой траты
    spending_amount = str(fake.random_int(min=10, max=10000))
    spending_currency = "KZT"
    spending_category = fake.word()
    today = date.today()
    spending_date = str(today.day)
    spending_description = fake.word()

    # Создаём трату
    spendings_page = SpendingsPage(page)  
    spendings_page.add_spending(spending_amount, spending_currency, spending_category, spending_date, spending_description)

    #Ожидаем что локатор с тратой присутствует
    spendings_page.spending_row(spending_category, spending_amount, spending_date).wait_for()


    #Удаляем трату и категорию
    spendings_page.delete_spending(spending_category, spending_amount, spending_date)
    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.archive_category(spending_category)


def test_create_invalid_spend(page: Page, signin_user):
    # Входные данные для создаваемой траты
    spending_amount = "0"
    spendings_page = SpendingsPage(page)

    # Создаём невалидную трату
    spendings_page.add_spending_button_link.click()
    spendings_page.amount_input.fill(spending_amount)
    spendings_page.amount_input.press("Enter")

    # Проверяем что span с ошибкой есть
    assert spendings_page.spending_amount_error.is_visible()

def test_delete_spend(page: Page, signin_user):
    # Входные данные для создаваемой траты
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word()
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Создаём трату
    create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    today = date.today()
    spend_date = str(today.day)

    page.reload()
    time.sleep(2)

    # Удаляем трату
    spending_page = SpendingsPage(page)
    row = spending_page.delete_spending(category_name, spend_amount, spend_date)
    assert row.is_hidden()

    # Удаляем категорию
    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.archive_category(category_name)


def test_delete_all_spends(page: Page, signin_user):
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word()
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Создаём траты
    create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)

    page.reload()
    time.sleep(2)

    # Удаляем все траты
    spending_page = SpendingsPage(page)
    spending_page.delete_all_spending()

    assert spending_page.no_spendings_text.is_visible()

    # Удаляем категории
    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.archive_category(category_name)


# Успешное редактирование траты
def test_edit_spend(page: Page, signin_user):

    # Входные данные для создаваемой траты
    spending_amount = str(fake.random_int(min=10, max=10000))
    spending_currency = "KZT"
    spending_category = fake.word()
    now = datetime.now(timezone.utc)
    spending_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    spending_description = fake.word()
    
    # Создаём трату через API
    created_spending = create_spending(signin_user, spending_amount,spending_category, spending_currency, spending_date, spending_description)

    page.reload()
    time.sleep(2)

    # Входные данные для редактирования траты
    new_spending_amount = "123"
    new_spending_currency = "RUB"
    new_spending_category = "New"
    new_spending_description = "NewDescr"
    today = date.today()
    new_spending_date = str((today - timedelta(days=1)).day)
    spending_day = str(today.day)

    # Редактируем трату
    spendings_page = SpendingsPage(page)  
    spendings_page.edit_spending(spending_category, spending_day, spending_description, new_spending_amount, new_spending_currency, new_spending_category, new_spending_date, new_spending_description)

    # Удаляем трату и категорию
    page.goto(f"{base_url}profile")
    delete_spending(created_spending['id'])
    profile_page = ProfilePage(page)
    profile_page.archive_category(spending_category)

# Редактирование траты с ошибкой
def test_edit_spend_with_error(page: Page, signin_user):

    spending_amount = str(fake.random_int(min=10, max=10000))
    spending_currency = "KZT"
    spending_category = fake.word()
    now = datetime.now(timezone.utc)
    spending_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    spending_description = fake.word()
    
     
    created_spending = create_spending(signin_user, spending_amount,spending_category, spending_currency, spending_date, spending_description)

    page.reload()
    time.sleep(2)

    new_spending_amount = "0"
    today = date.today()
    spending_date = str(today.day)

    spendings_page = SpendingsPage(page) 
    spendings_page.edit_invalid_spending(spending_category, spending_date, spending_description, new_spending_amount)
    assert spendings_page.spending_amount_error.is_visible()

    # Удаляем трату и категорию
    page.goto(f"{base_url}profile")
    delete_spending(created_spending['id'])
    profile_page = ProfilePage(page)
    profile_page.archive_category(spending_category)



# Поиск по строке
def test_search_spending_by_category(page: Page, signin_user):
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word()
    another_category_name = fake.word()+"Test"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Создаём траты
    spedn_one = create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    spend_two = create_spending(signin_user, spend_amount,another_category_name, spend_currency, spend_date, spend_description)

    spending_day = str(date.today().day)

    page.reload()
    time.sleep(2)

    # Удаляем все траты
    spending_page = SpendingsPage(page)
    spending_page.search_spending_by_category(category_name)

    expected_row = spending_page.spending_row(category_name, spend_amount, spending_day)
    another_row = spending_page.spending_row(another_category_name, spend_amount, spending_day)
    assert expected_row.is_visible()
    assert another_row.is_hidden()

    # Удаляем трату и категорию
    page.goto(f"{base_url}profile")
    delete_spending(spedn_one['id'])
    delete_spending(spend_two['id'])
    profile_page = ProfilePage(page)
    profile_page.archive_category(category_name)
    profile_page.archive_category(another_category_name)


# Поиск по строке
def test_search_spending_by_category(page: Page, signin_user):
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    another_currency = "RUB"
    category_name = fake.word()
    another_category = fake.word()+"Test"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Создаём траты
    spedn_one = create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    spend_two = create_spending(signin_user, spend_amount,another_category, another_currency, spend_date, spend_description)

    spending_day = str(date.today().day)

    page.reload()
    time.sleep(2)

    # Удаляем все траты
    spending_page = SpendingsPage(page)
    spending_page.search_spending_by_currency(spend_currency)

    expected_row = spending_page.spending_row(category_name, spend_amount, spending_day)
    another_row = spending_page.spending_row(another_category, spend_amount, spending_day)
    assert expected_row.is_visible()
    assert another_row.is_hidden()

    # Удаляем трату и категорию
    page.goto(f"{base_url}profile")
    delete_spending(spedn_one['id'])
    delete_spending(spend_two['id'])
    profile_page = ProfilePage(page)
    profile_page.archive_category(category_name)
    profile_page.archive_category(another_category)





