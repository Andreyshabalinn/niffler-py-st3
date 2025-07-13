from datetime import datetime, timezone
from pytest import FixtureDef, FixtureRequest, Item
import pytest
from playwright.sync_api import Page
from faker import Faker
from dotenv import load_dotenv
import os
from tests.utils.api_controller import auth_with_token, create_category, create_spending, delete_spending
from tests.database.spend_db import SpendDb
import allure
import logging
from utils.base_logging_client import BaseClient
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.pages.profile_page import ProfilePage
from tests.pages.signup_page import SignupPage
from tests.pages.spendings_page import SpendingsPage


load_dotenv()
fake = Faker()


global_user = os.getenv("TEST_LOGIN")
global_password = os.getenv("TEST_PASSWORD")

auth_url = os.getenv("BASE_AUTH_URL")
base_url = os.getenv("BASE_URL")
db_url = os.getenv("DB_URL")
auth_secret=os.getenv("AUTH_SECRET")


@pytest.fixture(scope="function")
def create_user(page: Page) -> tuple[str, str]:
    page.goto(f"{auth_url}register")

    username = global_user
    password = global_password 

    yield username, password

@pytest.fixture(scope="session")
def session_token():
    return auth_with_token()

@pytest.fixture(scope="function")
def api_client(auth_with_token) -> BaseClient:
    return BaseClient(base_url=os.getenv("API_BASE_URL"), token=auth_with_token)

@pytest.fixture(scope="function")
def authenticated_user(page: Page, create_user: tuple[str, str]) -> tuple[str, str]:

    username, password = create_user
    page.goto(f"{auth_url}login")

    page.get_by_placeholder("Type your username").fill(username)
    page.get_by_placeholder("Type your password").fill(password)

    page.get_by_role("button", name="Log in").click()

    page.wait_for_url(f"{base_url}main")

    yield username, password

@pytest.fixture(scope="function")
def created_category(authenticated_user: tuple[str, str]) -> tuple[str, str]:
    category_name, category_id = create_category(authenticated_user=authenticated_user)
    yield category_name, category_id
    db_client = SpendDb(db_url)
    db_client.delete_category(category_id)


@pytest.fixture(scope="function")
def created_spend(authenticated_user):
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word() + "456"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    created_spend = create_spending(
        authenticated_user,
        spend_amount,
        category_name,
        spend_currency,
        spend_date,
        spend_description,
    )
    # Создаём траты
    yield created_spend

    delete_spending(created_spend.id)
    db_client = SpendDb(db_url)
    db_client.delete_category(created_spend.category.id)


def allure_logger(config):
    listener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"{scope_letter} " + "".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())
    pass


def pytest_configure(config):
    logging.basicConfig(
        level=logging.DEBUG,  # или INFO
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


@pytest.fixture(scope="session")
def client():
    base_url = os.getenv("API_BASE_URL")
    token = os.getenv("TOKEN")
    return BaseClient(base_url=base_url, token=token)

#Pages

@pytest.fixture(scope="function")
def profile_page(page: Page):
    return ProfilePage(page)

@pytest.fixture(scope="function")
def main_page(page: Page):
    return MainPage(page)

@pytest.fixture(scope="function")
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture(scope="function")
def signup_page(page: Page):
    return SignupPage(page)

@pytest.fixture(scope="function")
def spendings_page(page: Page):
    return SpendingsPage(page)
    



