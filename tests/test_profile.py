from playwright.sync_api import Page
from faker import Faker
from tests.config import BASE_URL

import allure


fake = Faker()
base_url = BASE_URL


@allure.epic("Страница профиля")
@allure.feature("Имя профиля")
class TestsProfileName:
    @allure.story("Создание траты")
    def test_edit_profile_name(self, page: Page, authenticated_user, profile_page):
        user, _ = authenticated_user

        page.goto(f"{base_url}profile")
        profile_page.change_profile_name(user)
        profile_page.profile_success_update_popup.wait_for()

    @allure.story("Создание траты")
    def test_edit_invalid_profile_name(
        self, page: Page, authenticated_user, profile_page
    ):
        page.goto(f"{base_url}profile")
        profile_page.change_profile_name(fake.pystr(min_chars=51, max_chars=51))
        assert profile_page.name_len_error.is_visible()


@allure.epic("Страница профиля")
@allure.feature("Категории профиля")
class TestsProfileCategory:
    @allure.story("Создание категории")
    def test_add_profile_category(self, page: Page, authenticated_user, profile_page):
        page.goto(f"{base_url}profile")

        category_name = fake.word()
        profile_page.add_category(category_name)
        profile_page.category_by_name(category_name).wait_for()
        profile_page.archive_category(category_name)

    @allure.story("Создание невалидной категории")
    def test_add_invalid_profile_category(
        self, page: Page, authenticated_user, profile_page
    ):
        page.goto(f"{base_url}profile")

        category_name = "+"
        profile_page.category_name_input.fill(category_name)
        profile_page.category_name_input.press("Enter")
        assert profile_page.category_by_name(category_name).is_hidden()
        assert profile_page.category_max_length_error.is_visible()

    @allure.story("Архивация категории")
    def test_archive_category(self, page: Page, created_category, profile_page):
        category_name, _ = created_category

        page.goto(f"{base_url}profile")

        profile_page.archive_category(category_name)

        assert profile_page.category_by_name(category_name).is_hidden()
        profile_page.is_archive_include_checkbox.check()
        assert profile_page.category_by_name(category_name).is_visible()

    @allure.story("Редактирование категории")
    def test_edit_category(self, page: Page, created_category, profile_page):
        category_name, category_id = created_category

        page.goto(f"{base_url}profile")

        new_category_name = fake.word()
        profile_page.edit_category(category_name, new_category_name)

        profile_page.category_by_name(new_category_name).wait_for()
