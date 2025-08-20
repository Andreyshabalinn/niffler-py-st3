from pytest import FixtureDef, FixtureRequest, Item
import pytest
import os
from playwright.sync_api import Page
from tests.utils.kafka_client import KafkaClient
from faker import Faker
from tests.utils.allure_helper import allure_logger
import allure
import logging
from tests.config import USERNAME, PASSWORD, AUTH_URL, API_BASE_URL, BASE_URL, DB_URL, TOKEN, KAFKA_SERVER
from tests.utils.auth_client import AuthClient
fake = Faker()

auth_url = AUTH_URL
api_url = API_BASE_URL
base_url = BASE_URL
db_url = DB_URL
token = TOKEN
server_name = KAFKA_SERVER




pytest_plugins = ["tests.fixtures.page_fixtures", "tests.fixtures.api_entities_fixtures"]

def pytest_configure(config):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


# Вынес объявление клиента в api_client.py:
# client = BaseClient(base_url=base_url, token=auth_with_token())

# @pytest.fixture(scope="session")
# def session_token():
#     return auth_with_token()

# @pytest.fixture(scope="function")
# def api_client(auth_with_token) -> BaseClient:
#     return BaseClient(base_url=api_url, token=auth_with_token)

# @pytest.fixture(scope="session")
# def client():
#     base_url = api_url
#     return BaseClient(base_url=base_url, token=token)

@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()

@pytest.fixture(scope="session")
def kafka():
    """Взаимодействие с Kafka"""
    with KafkaClient(server_name) as k:
        yield k

def pytest_collection_modifyitems(config, items):
    serial = []
    parallel = []

    for item in items:
        if 'serial' in item.keywords:
            serial.append(item)
        else:
            parallel.append(item)

    # Запускаем сначала serial (они пойдут в одном процессе, обычно master), потом остальные
    items[:] = serial + parallel


@pytest.fixture(scope="session")
def worker_id():
    return os.environ.get("PYTEST_XDIST_WORKER", "gw0")

@pytest.fixture(scope="function")
def authenticated_user(page: Page) -> tuple[str, str]:

    username, password = USERNAME, PASSWORD
    page.goto(f"{auth_url}login")

    page.get_by_placeholder("Type your username").fill(username)
    page.get_by_placeholder("Type your password").fill(password)

    page.get_by_role("button", name="Log in").click()

    page.wait_for_url(f"{base_url}main")

    yield username, password


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"{scope_letter} " + "".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())
    pass
    



