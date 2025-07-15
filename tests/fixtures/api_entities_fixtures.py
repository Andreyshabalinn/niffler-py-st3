import time
import pytest
from tests.utils.api_controller import create_category, create_spending, delete_spending
from tests.database.spend_db import SpendDb
from faker import Faker
from tests.config import AUTH_URL, API_BASE_URL, BASE_URL, DB_URL, TOKEN
from datetime import datetime, timezone
fake = Faker()

auth_url = AUTH_URL
api_url = API_BASE_URL
base_url = BASE_URL
db_url = DB_URL
token = TOKEN


@pytest.fixture(scope="function")
def created_category() -> tuple[str, str]:
    category_name, category_id = create_category(fake.word())
    yield category_name, category_id
    db_client = SpendDb(db_url)
    db_client.delete_category(category_id)


@pytest.fixture(scope="function")
def created_spend():
    # Входные данные для создаваемых трат
    spend_amount = fake.random_int(min=10, max=10000)
    spend_description = fake.word()
    spend_currency = "KZT"
    category_name = fake.word() + "456"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    created_spend = create_spending(
        spend_amount,
        category_name,
        spend_currency,
        spend_date,
        spend_description,
    )
    # Создаём траты
    yield created_spend

    delete_spending(created_spend.id)
    db_client = SpendDb(db_url)
    db_client.delete_category(created_spend.category.id)