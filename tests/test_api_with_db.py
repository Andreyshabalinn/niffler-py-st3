from datetime import datetime, timezone
from requests import HTTPError
import allure
import pytest
from faker import Faker
from tests.utils.api_controller import (
    create_category,
    create_spending,
    delete_spending,
    edit_category_name,
    edit_spending,
    get_categories,
    get_spend
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
        _, created_category_id = create_category(category_name=faker.word())
        db_client = SpendDb(db_url)
        db_category = db_client.get_category_by_id(created_category_id)
        assert str(db_category.id) == created_category_id
        db_client.delete_category(db_category.id)

    def test_update_category(self, created_category):
        new_category_name = faker.word()
        edited_category = edit_category_name(
            category_name=new_category_name, category_id=str(created_category[1])
        )
        assert edited_category.name == new_category_name

    @pytest.mark.serial
    def test_get_all(self, created_category):
        categories = get_categories()
        db_client = SpendDb(db_url)
        db_categories = db_client.get_categories(global_user)
        assert len(db_categories) == len(categories)

    def test_get_all_and_check_data(self, worker_id):
        category_name_1, category_id_1 = create_category(category_name=faker.word() + worker_id)
        category_name_2, category_id_2 = create_category(category_name=faker.word() + worker_id + " second")
        db_client = SpendDb(db_url)
        db_category_1 = db_client.get_category_by_id(category_id_1)
        db_category_2 = db_client.get_category_by_id(category_id_2)

        assert str(db_category_1.id) == category_id_1
        assert str(db_category_2.id) == category_id_2
        assert str(db_category_1.name) == category_name_1
        assert str(db_category_2.name) == category_name_2

        db_client.delete_category(db_category_1.id)
        db_client.delete_category(db_category_2.id)

@allure.epic("API Niffler")
@allure.feature("Новые тесты")
class TestsNew:
    def test_add_invalid_category(self):
        with pytest.raises(HTTPError) as exc_info:
            create_category(category_name=".")
            response = exc_info.value.response
            assert response.status_code == 400


    def test_add_existing_category(self, created_category):
        category_name, _ = created_category
        result = create_category(category_name=category_name)
        assert result.status_code == 409

    @pytest.mark.xfail(reason="Мы не можем создать категорию из одного символа, но отредактировать можем, похоже на баг?", strict=True)
    def test_update_to_invalid_category(self,created_category):
        _, category_id = created_category
        result = edit_category_name("p", str(category_id))
        assert result == 400

    def test_update_to_existing_category(self):
        category_name_1, category_id_1 = create_category(category_name=faker.word())
        _, category_id_2 = create_category(category_name=faker.word()+"Test")
        result = edit_category_name(category_name_1, str(category_id_2))
        db_client = SpendDb(db_url)
        db_client.delete_category(category_id_1)
        db_client.delete_category(category_id_2)
        assert result.status_code == 409

    def test_update_non_existing_category(self):
        result = edit_category_name(faker.word(), str(faker.uuid4()))
        assert result.status_code == 404

    def test_add_invalid_spend(self):
        amount = 0
        category = "TestSpend"
        currency = "RUB"
        description = "TestDescriptio"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        with pytest.raises(HTTPError) as exc_info:
            create_spending(
            spend_amount=amount,
            spend_category=category,
            spend_currency=currency,
            spend_date=spend_date,
            spend_description=description,
        )
            response = exc_info.value.response
            assert response.status_code == 400

    def test_edit_invalid_spend(self, created_spend):
        new_amount = 0
        new_category = "TestSpendCat"
        new_currency = "RUB"
        new_description = "TestDescriptionNew"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        with pytest.raises(HTTPError) as exc_info:
            edit_spending(
            spend_amount=new_amount,
            spend_category=new_category,
            spend_currency=new_currency,
            spend_date=spend_date,
            spend_description=new_description,
            spend_id=created_spend.id,
        )
        response = exc_info.value.response
        assert response.status_code == 400

    def test_edit_non_existing_spend(self):
        new_amount = 123
        new_category = "TestSpendCat"
        new_currency = "RUB"
        new_description = "TestDescriptionNew"
        now = datetime.now(timezone.utc)
        spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        response = edit_spending(
            spend_amount=new_amount,
            spend_category=new_category,
            spend_currency=new_currency,
            spend_date=spend_date,
            spend_description=new_description,
            spend_id=str(faker.uuid4()),
        )
        assert response.status_code == 404

    def test_get_spend(self, created_spend):
        result = get_spend(created_spend.id)
        assert created_spend.model_dump(exclude={"spendDate"}) == result.model_dump(exclude={"spendDate"})
        

    def test_get_non_existing_spend(self):
        result = get_spend(faker.uuid4())
        assert result.status_code == 404

    