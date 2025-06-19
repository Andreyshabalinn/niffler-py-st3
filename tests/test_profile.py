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


def test_add_profile_category(page: Page, signin_user):
    page.goto(f"{base_url}profile")

    category_name = fake.word()
    profile_page = ProfilePage(page)
    profile_page.add_category(category_name)
    assert page.locator("span", has_text=category_name).is_visible()
    profile_page.archive_category(category_name)

def test_add_invalid_profile_category(page: Page, signin_user):
    page.goto(f"{base_url}profile")

    category_name = "+"
    profile_page = ProfilePage(page)
    profile_page.category_name_input.fill(category_name)
    profile_page.category_name_input.press("Enter")
    assert page.locator("span", has_text=category_name).is_hidden()
    assert page.locator("span", has_text="Allowed category length is from 2 to 50 symbols").is_visible()



def test_archive_category(page: Page, signin_user):

    category_name, _ = create_category(signin_user)

    page.goto(f"{base_url}profile")

    profile_page = ProfilePage(page)

    profile_page.archive_category(category_name)

    assert page.locator("span", has_text=category_name).is_hidden()
    page.get_by_label("Show archived").check()
    assert page.locator("span", has_text=category_name).is_visible()


#Добавить page object
def test_edit_category(page: Page, signin_user):

    category_name, category_id = create_category(signin_user)

    page.goto(f"{base_url}profile")

    new_category_name = fake.word()
    profile_page = ProfilePage(page)
    profile_page.edit_category(category_name, new_category_name)

    # category = page.locator("div.MuiBox-root", has=page.locator("span", has_text=category_name))
    # category.locator('button[aria-label="Edit category"]').click()

    # category_field = page.get_by_placeholder("Edit category")
    # category_field.fill(new_category_name)
    # category_field.press("Enter")

    # page.get_by_text(f"Category name is changed").wait_for()

    assert page.locator("span", has_text=new_category_name).is_visible()

    archive_category(new_category_name, category_id)

