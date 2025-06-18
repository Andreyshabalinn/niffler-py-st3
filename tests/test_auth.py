from playwright.sync_api import Page
from faker import Faker
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
fake = Faker()




def test_successful_signin(page: Page, create_user):

    user, password = create_user

    page.goto("http://auth.niffler.dc:9000/login")
    login_page = LoginPage(page)
    login_page.login(user, password)

    page.wait_for_url("http://frontend.niffler.dc/main")
    assert page.title() == "Niffler"

def test_successful_signup(page: Page):
    page.goto("http://auth.niffler.dc:9000/register")

    username = fake.user_name()
    password = fake.password()

    signup_page = SignupPage(page)
    signup_page.signup(username, password)

    page.wait_for_url("http://frontend.niffler.dc/main")
    page.wait_for_url("http://auth.niffler.dc:9000/login")
    assert page.title() == "Login to Niffler"
    