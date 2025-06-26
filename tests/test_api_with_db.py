from datetime import datetime, timezone
import time
from dotenv import load_dotenv
import os
from tests.api_controller import create_category, create_spending, delete_spending, edit_spending, edit_category_name, get_categories
from tests.database.spend_db import SpendDb


load_dotenv()

db_url = os.getenv("DB_URL")

# ------------------- spend-controller -------------------

def test_add_spend(signin_user):
    amount = 1234
    category = "TestSpend"
    currency = "RUB"
    description = "TestDescriptio"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    spend = create_spending(signin_user=signin_user, spend_amount=amount, spend_category=category, spend_currency=currency, spend_date=spend_date, spend_description=description)

    db_client = SpendDb(db_url)
    db_spend = db_client.get_spend_by_id(spend.id)

    assert db_spend.description == description
    assert db_spend.currency == currency
    assert db_spend.amount == amount
    assert db_spend.category_id == db_client.get_category_by_name(category).id

    delete_spending(spend.id)
    db_client = SpendDb(db_url)
    db_client.delete_category(spend.category.id)



def test_edit_spend(created_spend, signin_user):
    new_amount = 1234
    new_category = "TestSpendCat"
    new_currency = "RUB"
    new_description = "TestDescriptionNew"
    now = datetime.now(timezone.utc)
    spend_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    edit_spending(signin_user, spend_amount=new_amount, spend_category=new_category, spend_currency=new_currency, spend_date=spend_date, spend_description=new_description, spend_id=created_spend.id)

    db_client = SpendDb(db_url)
    db_spend = db_client.get_spend_by_id(created_spend.id)
    
    assert db_spend.description == new_description
    assert db_spend.currency == new_currency
    assert db_spend.amount == new_amount
    assert db_spend.category_id == db_client.get_category_by_name(new_category).id

def test_remove_spend(created_spend):
    delete_spending(created_spend.id)
    db_client = SpendDb(db_url)
    db_spend = db_client.get_spend_by_id(created_spend.id)
    print(db_spend)
    assert db_spend is None


# ------------------- categories-controller -------------------

def test_add_category(signin_user):
    _, created_category_id = create_category(signin_user)
    db_client = SpendDb(db_url)
    db_category = db_client.get_category_by_id(created_category_id)
    assert db_category.id == created_category_id
    db_client.delete_category(db_category.id)


def test_update_category(created_category):
    new_category_name = "NewNameCatApi"
    edited_category = edit_category_name(category_name=new_category_name, category_id=str(created_category[1]))
    assert edited_category.name == new_category_name

def test_get_all(created_category, signin_user):
    categories = get_categories()
    db_client = SpendDb(db_url)
    db_categories = db_client.get_categories(signin_user[0])
    assert len(db_categories) == len(categories)
