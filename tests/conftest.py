from datetime import datetime, timezone
from typing import Tuple
import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from faker import Faker
<<<<<<< HEAD
from api_controller import create_spending, delete_spending
=======
from tests.pages.signup_page import SignupPage
from database.spend_db import SpendDb
>>>>>>> 1b125a3 (Add models and db client)
from dotenv import load_dotenv
import os
from api_controller import create_category, archive_category


load_dotenv()
fake = Faker()


global_user = os.getenv("TEST_LOGIN")
global_password = os.getenv("TEST_PASSWORD")

auth_url = os.getenv("BASE_AUTH_URL")
base_url = os.getenv("BASE_URL")
db_url = os.getenv("DB_URL")

@pytest.fixture(scope="function")
def create_user(page: Page)->Tuple[str, str]:
    page.goto(f"{auth_url}register") 

    username = global_user#fake.user_name()
    password = global_password#fake.password()

    # Первый раз надо раскомментировать и создать пользователя 
    # signup_page = SignupPage(page)
    # signup_page.signup(username, password)

    # page.wait_for_url("http://frontend.niffler.dc/main")
    # page.wait_for_url("http://auth.niffler.dc:9000/login")
    # assert page.title() == "Login to Niffler"

    yield username, password


@pytest.fixture(scope="function")
def signin_user(page: Page, create_user:Tuple[str, str])->Tuple[str, str]:

    username, password = create_user
    page.goto(f"{auth_url}login") 


    page.get_by_placeholder("Type your username").fill(username)
    page.get_by_placeholder("Type your password").fill(password)

    page.get_by_role("button", name="Log in").click()


    page.wait_for_url(f"{base_url}main")

    yield username, password


@pytest.fixture(scope="function")
def created_category(signin_user:Tuple[str, str])->Tuple[str, str]:
    category_name, category_id = create_category(signin_user=signin_user)
    yield category_name, category_id
<<<<<<< HEAD


@pytest.fixture(scope="function")
def created_spend(signin_user):
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word()
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    created_spend = create_spending(signin_user, spend_amount,category_name, spend_currency, spend_date, spend_description)
    # Создаём траты
    yield created_spend

    delete_spending(created_spend['id'])
    
=======
    db_client = SpendDb(db_url)
    db_client.delete_category(category_id)

@pytest.fixture(scope="function")
def created_spend(signin_user:Tuple[str, str])->Tuple[str, str]:
    category_name, category_id = create_category(signin_user=signin_user)
    yield category_name, category_id
    db_client = SpendDb(db_url)
    db_client.delete_category(category_id)


>>>>>>> 1b125a3 (Add models and db client)
    

@pytest.fixture(scope="function")
def page()->Page:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()