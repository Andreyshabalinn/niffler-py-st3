import pytest
from tests.pages.profile_page import ProfilePage
from tests.pages.main_page import MainPage
from tests.pages.login_page import LoginPage
from tests.pages.signup_page import SignupPage
from tests.pages.spendings_page import SpendingsPage
from playwright.sync_api import Page

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