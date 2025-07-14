import uuid
from faker import Faker

from tests.models.spend import SpendCreate, Category
from tests.utils.auth_client import auth_with_token
from tests.utils.base_logging_client import BaseClient

from tests.config import TOKEN, API_BASE_URL, USERNAME, PASSWORD
fake = Faker()

token = TOKEN
base_url = API_BASE_URL
global_user = USERNAME
global_password = PASSWORD


client = BaseClient(base_url=base_url, token=auth_with_token())

def get_categories():
    result = client.request("GET", "categories/all")
    assert result.status_code == 200
    categories = [Category.model_validate(item) for item in result.json()]
    return categories

def edit_category_name(category_name: str, category_id: str):
    payload = {
        "id": category_id,
        "name": category_name,
        "username": "asd",
        "archived": False,
    }
    result = client.request("PATCH", "categories/update", json=payload)
    assert result.status_code == 200
    category = Category.model_validate(result.json())
    return category

def archive_category(category_name: str, category_id: str):
    payload = {
        "id": category_id,
        "name": category_name,
        "username": "asd",
        "archived": True,
    }
    result = client.request("PATCH", "categories/update", json=payload)
    assert result.status_code == 200

def create_category() -> tuple[str, uuid.UUID]:
    username = global_user
    name = fake.word()
    payload = {"name": name, "username": username, "archived": False}
    result = client.request("POST", "categories/add", json=payload)
    assert result.status_code == 200, result.status_code
    parsed = Category.model_validate(result.json())
    return parsed.name, parsed.id


def create_spending(
    spend_amount: str,
    spend_category: str,
    spend_currency: str,
    spend_date: str,
    spend_description: str,
):
    username = global_user
    payload = {
        "spendDate": spend_date,
        "category": {
            "id": str(uuid.uuid4()),
            "name": spend_category,
            "username": username,
            "archived": False,
        },
        "currency": spend_currency,
        "amount": spend_amount,
        "description": spend_description,
        "username": username,
    }
    result = client.request("POST", "spends/add", json=payload)
    assert result.status_code == 201, result.status_code
    return SpendCreate.model_validate(result.json())

def edit_spending(
    spend_amount: str,
    spend_category: str,
    spend_currency: str,
    spend_date: str,
    spend_description: str,
    spend_id: uuid.UUID,
):
    username = global_user
    payload = {
        "id": spend_id,
        "spendDate": spend_date,
        "category": {
            "id": str(uuid.uuid4()),
            "name": spend_category,
            "username": username,
            "archived": False,
        },
        "currency": spend_currency,
        "amount": spend_amount,
        "description": spend_description,
        "username": username,
    }
    result = client.request("PATCH", "spends/edit", json=payload)
    assert result.status_code == 200, result.request.body
    return SpendCreate.model_validate(result.json())

def delete_spending(spending_id: str):
    result = client.request("DELETE", "spends/remove", params={"ids": spending_id})
    assert result.status_code == 200
