from playwright.sync_api import Page
from faker import Faker
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
fake = Faker()
from dotenv import load_dotenv
import os
load_dotenv()

base_auth_url = os.getenv("BASE_AUTH_URL")
base_url = os.getenv("BASE_URL")



def test_successful_signin(page: Page, create_user):

     user, password = create_user

     page.goto(f"{base_auth_url}login")
     login_page = LoginPage(page)
     login_page.login(user, password)

     page.wait_for_url(f"{base_url}main")
     assert page.title() == "Niffler"

def test_successful_signup(page: Page):
     page.goto(f"{base_auth_url}register")

     username = fake.user_name()
     password = fake.password()

     signup_page = SignupPage(page)
     signup_page.signup(username, password)

     page.wait_for_url(f"{base_url}main")
     page.wait_for_url(f"{base_auth_url}login")
     assert page.title() == "Login to Niffler"

def test_try_signup_on_already_exsist_creds(page: Page):
    page.goto(f"{base_auth_url}register")

    username = fake.user_name()
    password = fake.password()

    signup_page = SignupPage(page)
    signup_page.signup(username, password)

    page.goto(f"{base_auth_url}register")

    signup_page.signup(username, password)

    page.locator("span.form__error", has_text=f"Username `{username}` already exists").wait_for()

def test_try_signup_with_invalid_username(page: Page):
    page.goto(f"{base_auth_url}register")

    username = fake.pystr(min_chars=51, max_chars=51)
    password = fake.password()

    signup_page = SignupPage(page)
    signup_page.signup(username, password)

def test_try_signup_with_unmatched_passwords(page: Page):
    page.goto(f"{base_auth_url}register")

    username = fake.user_name()
    password = fake.password()

    signup_page = SignupPage(page)
    signup_page.signup_with_unmatched_passwords(username, password)

def test_try_signup_with_invalid_password(page: Page):
    page.goto(f"{base_auth_url}register")

    username = fake.user_name()
    password = "1"

    signup_page = SignupPage(page)
    signup_page.signup(username, password)

def test_failed_signin(page: Page):

    username = fake.user_name()
    password = fake.password()

    page.goto(f"{base_auth_url}login")
    login_page = LoginPage(page)
    login_page.login(username, password)
    assert login_page.signin_invalid_creds_error.is_visible()

    