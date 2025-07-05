import time
import allure
from playwright.sync_api import Page
from faker import Faker
from datetime import date, datetime, timedelta, timezone
from pages.spendings_page import SpendingsPage
from pages.profile_page import ProfilePage
from api_controller import create_spending, delete_spending
from database.spend_db import SpendDb
fake = Faker()
from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv("BASE_URL")
db_url = os.getenv("DB_URL")

@allure.epic("Страница трат")
@allure.feature("Создание трат")
class TestsCreateSpends:
    @allure.story("Создание траты")
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

    @allure.story("Создание невалидной траты")
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


@allure.epic("Страница трат")
@allure.feature("Удаление трат")
class TestsDeleteSpends:
    @allure.story("Успешное удаление одной траты")
    def test_delete_spend(page: Page, created_spend):
        today = date.today()
        spend_date = str(today.day)

        page.reload()
        time.sleep(2)

        # Удаляем трату
        spending_page = SpendingsPage(page)
        row = spending_page.delete_spending(created_spend.category.name, int(created_spend.amount), spend_date)
        assert row.is_hidden()

    @allure.story("Удаление всех трат")
    def test_delete_all_spends(page: Page, created_spend):
        # Удаляем все траты
        spending_page = SpendingsPage(page)
        spending_page.delete_all_spending()

        assert spending_page.no_spendings_text.is_visible()
@allure.epic("Страница трат")
@allure.feature("Редактированиие трат")
class TestsEditeSpends:
    @allure.story("Успешное редактирование траты")
    def test_edit_spend(page: Page, created_spend):

        # Входные данные для создаваемой траты
        
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
        spendings_page.edit_spending(created_spend.category.name, spending_day, created_spend.description, new_spending_amount, new_spending_currency, new_spending_category, new_spending_date, new_spending_description)

    @allure.story("Редактирование траты с ошибкой")
    def test_edit_spend_with_error(page: Page, created_spend):

        now = datetime.now(timezone.utc)
        spending_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        page.reload()
        time.sleep(2)

        new_spending_amount = "0"
        today = date.today()
        spending_date = str(today.day)

        spendings_page = SpendingsPage(page) 
        spendings_page.edit_invalid_spending(created_spend.category.name, spending_date, created_spend.description, new_spending_amount)
        assert spendings_page.spending_amount_error.is_visible()

@allure.epic("Страница трат")
@allure.feature("Поиск трат")
class TestsSearchSpends:
    @allure.story("Поиск траты по категории")
    def test_search_spending_by_category(page: Page, created_spend, signin_user):
        # Входные данные для создаваемых трат
        spend_amount = fake.random_int(min=10, max=10000)
        spend_description = fake.word()
        another_currency = "RUB"
        another_category = fake.word()+"Test"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Создаём траты
        spend_one = created_spend
        spend_two = create_spending(signin_user, spend_amount,another_category, another_currency, spend_date, spend_description)

        spending_day = str(date.today().day)

        page.reload()
        time.sleep(2)

        # Удаляем все траты
        spending_page = SpendingsPage(page)
        spending_page.search_spending_by_category(spend_one.category.name)

        expected_row = spending_page.spending_row(spend_one.category.name, int(spend_one.amount), spending_day)
        another_row = spending_page.spending_row(spend_two.category.name, spend_amount, spending_day)
        assert expected_row.is_visible()
        assert another_row.is_hidden()

        # Удаляем трату и категорию
        delete_spending(spend_two.id)
        db_client = SpendDb(db_url)
        db_client.delete_category_by_name(spend_two.category.name)

    @allure.story("Поиск траты по валюте")
    def test_search_spending_by_currency(page: Page, created_spend, signin_user):
        # Входные данные для создаваемых трат
        spend_amount = fake.random_int(min=10, max=10000)
        spend_description = fake.word()
        spend_currency = "KZT"
        another_currency = "RUB"
        another_category = fake.word()+"Test"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Создаём траты
        spend_one = created_spend
        spend_two = create_spending(signin_user, spend_amount,another_category, another_currency, spend_date, spend_description)

        spending_day = str(date.today().day)

        page.reload()
        time.sleep(2)

        # Удаляем все траты
        spending_page = SpendingsPage(page)
        spending_page.search_spending_by_currency(spend_currency)

        expected_row = spending_page.spending_row(spend_one.category.name, int(spend_one.amount), spending_day)
        another_row = spending_page.spending_row(spend_two.category.name, spend_amount, spending_day)
        assert expected_row.is_visible()
        assert another_row.is_hidden()

        # Удаляем трату и категорию
        delete_spending(spend_two.id)
        db_client = SpendDb(db_url)
        db_client.delete_category_by_name(spend_two.category.name)





