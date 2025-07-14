from datetime import datetime, timezone
import allure
from faker import Faker
from tests.utils.api_controller import (
    create_category,
    create_spending,
    delete_spending,
    edit_category_name,
    edit_spending,
    get_categories,
)
from tests.database.spend_db import SpendDb
from tests.config import DB_URL, USERNAME

faker = Faker()
db_url = DB_URL
global_user = USERNAME

@allure.epic("API Niffler")
@allure.feature("Траты")
class TestsSpendApi:
    @allure.story("Создание траты")
    def test_add_spend(self):
        amount = 1234
        category = "TestSpend"
        currency = "RUB"
        description = "TestDescriptio"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        spend = create_spending(
            spend_amount=amount,
            spend_category=category,
            spend_currency=currency,
            spend_date=spend_date,
            spend_description=description,
        )

        db_client = SpendDb(db_url)
        db_spend = db_client.get_spend_by_id(spend.id)

        assert db_spend.description == description
        assert db_spend.currency == currency
        assert db_spend.amount == amount
        assert db_spend.category_id == db_client.get_category_by_name(category).id

        delete_spending(spend.id)
        db_client = SpendDb(db_url)
        db_client.delete_category(spend.category.id)

    @allure.story("Создание траты")
    def test_edit_spend(self, created_spend):
        new_amount = 1234
        new_category = "TestSpendCat"
        new_currency = "RUB"
        new_description = "TestDescriptionNew"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        edit_spending(
            spend_amount=new_amount,
            spend_category=new_category,
            spend_currency=new_currency,
            spend_date=spend_date,
            spend_description=new_description,
            spend_id=created_spend.id,
        )

        db_client = SpendDb(db_url)
        db_spend = db_client.get_spend_by_id(created_spend.id)

        assert db_spend.description == new_description
        assert db_spend.currency == new_currency
        assert db_spend.amount == new_amount
        assert db_spend.category_id == db_client.get_category_by_name(new_category).id

    @allure.story("Создание траты")
    def test_remove_spend(self, created_spend):
        delete_spending(created_spend.id)
        db_client = SpendDb(db_url)
        db_spend = db_client.get_spend_by_id(created_spend.id)
        assert db_spend is None


@allure.epic("API Niffler")
@allure.feature("Категории")
class TestsCategoryApi:
    def test_add_category(self):
        _, created_category_id = create_category()
        db_client = SpendDb(db_url)
        db_category = db_client.get_category_by_id(created_category_id)
        assert db_category.id == created_category_id
        db_client.delete_category(db_category.id)

    def test_update_category(self, created_category):
        new_category_name = faker.word()
        edited_category = edit_category_name(
            category_name=new_category_name, category_id=str(created_category[1])
        )
        assert edited_category.name == new_category_name

    def test_get_all(self, created_category):
        categories = get_categories()
        db_client = SpendDb(db_url)
        db_categories = db_client.get_categories(global_user)
        assert len(db_categories) == len(categories)

# class TestsNew:
#     def test_add_invalid_category(self):
#         pass

#     def test_add_existing_category(self):
#         pass

#     def test_update_invalid_category(self):
#         pass

#     def test_update_to_existing_category(self):
#         pass

#     def add_invalid_spend(self):
#         pass

#     def edit_invalid_spend(self):
#         pass

#     def edit_non_existing_spend(self):
#         pass

#     def get_spend(self):
#         pass

#     def get_non_existing_spend(self):
#         pass

#     def get_all_spends(self):
#         pass

    