import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from faker import Faker
from pages.signup_page import SignupPage
from dotenv import load_dotenv
import os
from api_controller import create_category, archive_category

load_dotenv()
fake = Faker()


global_user = "asd"
global_password = "asd"

@pytest.fixture(scope="function")
def create_user(page: Page):
    page.goto("http://auth.niffler.dc:9000/register") 

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
def signin_user(page: Page, create_user):

    username, password = create_user
    page.goto("http://auth.niffler.dc:9000/login") 


    page.get_by_placeholder("Type your username").fill(username)
    page.get_by_placeholder("Type your password").fill(password)

    page.get_by_role("button", name="Log in").click()


    page.wait_for_url("http://frontend.niffler.dc/main")

    yield username, password


@pytest.fixture(scope="function")
def created_category(signin_user):
    category_name, category_id = create_category(signin_user=signin_user)
    yield category_name, category_id
    archive_category(category_name, category_id)
    

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()