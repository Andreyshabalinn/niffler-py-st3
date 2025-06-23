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
    