import uuid
from faker import Faker
from dotenv import load_dotenv
import os
import allure
from tests.models.spend import Category, SpendCreate
from base_logging_client import BaseClient

load_dotenv()
fake = Faker()

token = os.getenv("TOKEN")
base_url = os.getenv("API_BASE_URL")

client = BaseClient(base_url=base_url, token=token)


def get_categories():
    result = client.request("GET", "categories/all")
    _log_response(result)
    assert result.status_code == 200
    categories = [Category.model_validate(item) for item in result.json()]
    allure.attach(
        str(categories),
        name="Parsed Categories",
        attachment_type=allure.attachment_type.TEXT,
    )
    return categories


def edit_category_name(category_name: str, category_id: str):
    payload = {
        "id": category_id,
        "name": category_name,
        "username": "asd",
        "archived": False,
    }
    result = client.request("PATCH", "categories/update", json=payload)
    _log_response(result, payload)
    assert result.status_code == 200
    category = Category.model_validate(result.json())
    allure.attach(
        str(category),
        name="Parsed Category",
        attachment_type=allure.attachment_type.TEXT,
    )
    return category


def archive_category(category_name: str, category_id: str):
    payload = {
        "id": category_id,
        "name": category_name,
        "username": "asd",
        "archived": True,
    }
    result = client.request("PATCH", "categories/update", json=payload)
    _log_response(result, payload)
    assert result.status_code == 200


def create_category(authenticated_user) -> tuple[str, uuid.UUID]:
    username, _ = authenticated_user
    name = fake.word()
    payload = {"name": name, "username": username, "archived": False}
    result = client.request("POST", "categories/add", json=payload)
    _log_response(result, payload)
    assert result.status_code == 200, result.status_code
    parsed = Category.model_validate(result.json())
    return parsed.name, parsed.id


def create_spending(
    authenticated_user: str,
    spend_amount: str,
    spend_category: str,
    spend_currency: str,
    spend_date: str,
    spend_description: str,
):
    username, _ = authenticated_user
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
    _log_response(result, payload)
    assert result.status_code == 201, result.status_code
    return SpendCreate.model_validate(result.json())


def edit_spending(
    authenticated_user: str,
    spend_amount: str,
    spend_category: str,
    spend_currency: str,
    spend_date: str,
    spend_description: str,
    spend_id: uuid.UUID,
):
    username, _ = authenticated_user
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
    _log_response(result, payload)
    assert result.status_code == 200, result.request.body
    return SpendCreate.model_validate(result.json())


def delete_spending(spending_id: str):
    result = client.request("DELETE", "spends/remove", params={"ids": spending_id})
    _log_response(result)
    assert result.status_code == 200


def _log_response(response, payload=None):
    allure.attach(
        str(response.request.headers),
        name="Request Headers",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        response.request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT,
    )
    if payload:
        allure.attach(
            str(payload),
            name="Request Body",
            attachment_type=allure.attachment_type.JSON,
        )
    elif response.request.body:
        allure.attach(
            str(response.request.body),
            name="Request Body",
            attachment_type=allure.attachment_type.JSON,
        )
    allure.attach(
        str(response.status_code),
        name="Status Code",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        response.text, name="Response Body", attachment_type=allure.attachment_type.JSON
    )
