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
    if result.status_code == 200:
        category = Category.model_validate(result.json())
        return category
    return result

def archive_category(category_name: str, category_id: str):
    payload = {
        "id": category_id,
        "name": category_name,
        "username": "asd",
        "archived": True,
    }
    result = client.request("PATCH", "categories/update", json=payload)
    assert result.status_code == 200

def create_category(category_name: str) -> tuple[str, uuid.UUID]:
    username = global_user
    name = category_name
    payload = {"name": name, "username": username, "archived": False}
    result = client.request("POST", "categories/add", json=payload)
    if result.status_code == 200:
        parsed = Category.model_validate(result.json())
        return parsed.name, parsed.id
    return result

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
    if result.status_code == 201:
        return SpendCreate.model_validate(result.json())
    return result

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
    if result.status_code == 200:
        return SpendCreate.model_validate(result.json())
    return result

def get_spend(spending_id: str):
    result = client.request("GET", f"spends/{spending_id}")
    if result.status_code == 200:
        return SpendCreate.model_validate(result.json())
    return result

def delete_spending(spending_id: str):
    client.request("DELETE", "spends/remove", params={"ids": spending_id})
