import time
from typing import Tuple
import uuid
import requests
from faker import Faker
from dotenv import load_dotenv
import os
import allure
from tests.models.spend import Category, SpendCreate

load_dotenv()

fake = Faker()

token = os.getenv("TOKEN")
base_url = os.getenv("API_BASE_URL")


def get_categories():
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*"}
    result = requests.get(f"{base_url}categories/all", headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    assert result.status_code == 200, print(result.json())
    categories = [Category.model_validate(item) for item in result.json()]
    allure.attach(str(categories), name="Parsed Categories", attachment_type=allure.attachment_type.TEXT)
    return categories

def edit_category_name(category_name: str, category_id: str):
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*"}
    username = "asd"
    category_data = {
        "id": category_id,
        "name": category_name,
        "username": username,
        "archived": False
    }
    result = requests.patch(f"{base_url}categories/update", json=category_data, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(category_data), name="Request Body", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    assert result.status_code == 200, print(result.json())
    category_name = Category.model_validate(result.json())
    allure.attach(str(category_name), name="Parsed Category", attachment_type=allure.attachment_type.TEXT)
    return category_name

def archive_category(category_name: str, category_id: str):
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*"}
    username = "asd"
    category_data = {
        "id": category_id,
        "name": category_name,
        "username": username,
        "archived": True
    }
    result = requests.patch(f"{base_url}categories/update", json=category_data, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(category_data), name="Request Body", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    assert result.status_code == 200, print(result.json())
    time.sleep(10)

def create_category(signin_user) -> Tuple[str, uuid.UUID]:
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*"}
    username, _ = signin_user
    category_name = fake.word()
    category_data = {
        "name": category_name,
        "username": username,
        "archived": False
    }
    result = requests.post(f"{base_url}categories/add", json=category_data, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(category_data), name="Request Body", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    assert result.status_code == 200, result.status_code
    time.sleep(3)
    print(f"Категория {category_name} успешно создана")
    category_id = result.json()['id']
    result_model = Category.model_validate(result.json())
    return result_model.name, result_model.id

def create_spending(signin_user: str, spend_amount: str, spend_category: str, spend_currency: str, spend_date: str, spend_description: str):
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*", "Content-Type": "application/json"}
    username, _ = signin_user
    data = {
        "spendDate": spend_date,
        "category": {
            "id": str(uuid.uuid4()),
            "name": spend_category,
            "username": username,
            "archived": False
        },
        "currency": spend_currency,
        "amount": spend_amount,
        "description": spend_description,
        "username": username
    }
    result = requests.post(f"{base_url}spends/add", json=data, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(data), name="Request Body", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    print(result.request.body)
    assert result.status_code == 201, result.request.body
    result_model = SpendCreate.model_validate(result.json())
    return result_model

def edit_spending(signin_user: str, spend_amount: str, spend_category: str, spend_currency: str, spend_date: str, spend_description: str, spend_id: uuid.UUID):
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*", "Content-Type": "application/json"}
    username, _ = signin_user
    data = {
        "id": spend_id,
        "spendDate": spend_date,
        "category": {
            "id": str(uuid.uuid4()),
            "name": spend_category,
            "username": username,
            "archived": False
        },
        "currency": spend_currency,
        "amount": spend_amount,
        "description": spend_description,
        "username": username
    }
    result = requests.patch(f"{base_url}spends/edit", json=data, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(data), name="Request Body", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    print(result.request.body)
    assert result.status_code == 200, result.request.body
    result_model = SpendCreate.model_validate(result.json())
    return result_model

def delete_spending(spending_id: str):
    headers = {"Authorization": f"Bearer {token}", "Accept": "*/*"}
    result = requests.delete(f"{base_url}spends/remove", params={"ids": spending_id}, headers=headers)
    allure.attach(str(result.request.url), name="Request URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(f"spending_id={spending_id}", name="Request Params", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(result.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(result.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
    assert result.status_code == 200, print(result.json())
