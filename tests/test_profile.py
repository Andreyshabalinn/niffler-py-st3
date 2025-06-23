from playwright.sync_api import Page
from faker import Faker
from conftest import archive_category, create_category
fake = Faker()
from pages.profile_page import ProfilePage
from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv("BASE_URL")



def test_edit_profile_name(page: Page, signin_user):
    user, _ = signin_user

    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.change_profile_name(user)
    profile_page.profile_success_update_popup.wait_for()

def test_edit_invalid_profile_name(page: Page, signin_user):

    page.goto(f"{base_url}profile")
    profile_page = ProfilePage(page)
    profile_page.change_profile_name(fake.pystr(min_chars=51, max_chars=51))
    assert profile_page.name_len_error.is_visible()



def test_add_profile_category(page: Page, signin_user):
    page.goto(f"{base_url}profile")

    category_name = fake.word()
    profile_page = ProfilePage(page)
    profile_page.add_category(category_name)
    assert profile_page.category_by_name(category_name).is_visible()
    profile_page.archive_category(category_name)

def test_add_invalid_profile_category(page: Page, signin_user):
    page.goto(f"{base_url}profile")

    category_name = "+"
    profile_page = ProfilePage(page)
    profile_page.category_name_input.fill(category_name)
    profile_page.category_name_input.press("Enter")
    assert profile_page.category_by_name(category_name).is_hidden()
    assert profile_page.category_max_length_error.is_visible()



def test_archive_category(page: Page, signin_user):

    category_name, _ = create_category(signin_user)

    page.goto(f"{base_url}profile")

    profile_page = ProfilePage(page)

    profile_page.archive_category(category_name)

    assert profile_page.category_by_name(category_name).is_hidden()
    profile_page.is_archive_include_checkbox.check()
    assert profile_page.category_by_name(category_name).is_visible()


#Добавить page object
def test_edit_category(page: Page, signin_user):

    category_name, category_id = create_category(signin_user)

    page.goto(f"{base_url}profile")

    new_category_name = fake.word()
    profile_page = ProfilePage(page)
    profile_page.edit_category(category_name, new_category_name)

    assert profile_page.category_by_name(category_name).is_visible()

    archive_category(new_category_name, category_id)

