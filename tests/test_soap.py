import allure
import pytest
from faker import Faker

from tests.xml_templates.read_templates import (current_user_xml, update_user_xml, send_invitation_xml,
                                                            accept_invitation_xml, decline_invitation_xml, friends,
                                                            remove_friend)
from tests.utils.sessions import SoapSession
from tests.utils.xml_check import check_current_user_result_operation, get_friends_list
from tests.config import DB_URL, USERNAME, USER_DB_URL, SOAP_ADDRESS
from tests.database.user_db import UsersDb

fake = Faker()
global_user = USERNAME

@pytest.fixture(scope='module')
def soap_session():
    session = SoapSession(base_url=SOAP_ADDRESS)
    return session

@allure.epic("API Niffler")
@allure.feature("Пользователи")
class TestSoapNiffler:

    @allure.title('Получение информации о существующем пользователе по его username')
    def test_get_user_info_by_exist_username(self, soap_session):
        with allure.step(f'Выполнить запрос по пользователю {global_user}'):
            response = soap_session.request(data=current_user_xml(global_user))

        with allure.step('Проверить корректность ответа'):
            user_data = check_current_user_result_operation(response.text)
            assert user_data['username'] == global_user
            with allure.step('Убедиться, что у пользователя есть id'):
                assert user_data['id'], 'У пользователя нет id'

    @allure.title('Запрос информации о незарегистрированном пользователе в системе по username')
    def test_get_user_info_by_not_exist_username(self, soap_session):
        user_name = fake.name()
        with allure.step(f'Выполнить запрос по пользователю {user_name}'):
            response = soap_session.request(data=current_user_xml(user_name))

        with allure.step('Проверить ответ'):
            user_data = check_current_user_result_operation(response.text)
            assert user_data['username'] == user_name
            with allure.step('Убедиться, что у пользователя в ответе отсутствует поле id'):
                assert not user_data['id'], 'У пользователя есть id'
            with allure.step('Убедиться, что у пользователя в ответе отсутствует поле fullname'):
                assert not user_data['fullname'], 'У пользователя есть поле fullname'

    @allure.title('Отправка запроса на дружбу')
    def test_send_invitation(self, soap_session, auth_client):
        user_1, user_2 = fake.name(), fake.name()
        with allure.step(f'Создать пользователей {user_1} и {user_2} в системе'):
            auth_client.register(user_1, fake.password(special_chars=False))
            auth_client.register(user_2, fake.password(special_chars=False))
            db_client = UsersDb(USER_DB_URL)
            user_1_from_db = db_client.get_user(user_1)
            user_2_from_db =  db_client.get_user(user_2)

        with allure.step(f'Отправить запрос на дружбу от {user_1} к {user_2}'):
            soap_session.request(data=send_invitation_xml(user_1, user_2))

        with allure.step('Убедиться, что статус приглашения в БД == PENDING'):
            friendship = db_client.get_friendship(user_1_from_db.id.__str__(), user_2_from_db.id.__str__())
            assert friendship.status == 'PENDING', 'Статус != "PENDING"'

    @allure.title('Принятие запроса на дружбу')
    def test_accept_invitation(self, soap_session, auth_client):
        user_1, user_2 = fake.name(), fake.name()
        with allure.step(f'Создать пользователей {user_1} и {user_2} в системе'):
            auth_client.register(user_1, fake.password(special_chars=False))
            auth_client.register(user_2, fake.password(special_chars=False))
            db_client = UsersDb(USER_DB_URL)
            user_1_from_db = db_client.get_user(user_1)
            user_2_from_db =  db_client.get_user(user_2)

        with allure.step(f'Отправить запрос на дружбу от {user_1} к {user_2}'):
            soap_session.request(data=send_invitation_xml(user_1, user_2))

        with allure.step(f'Принять запрос на дружбу пользователем {user_2} от {user_1}'):
            soap_session.request(data=accept_invitation_xml(user_2, friend=user_1))

        with allure.step('Убедиться, что статус приглашения в БД == ACCEPTED'):
            friendship = db_client.get_friendship(user_1_from_db.id.__str__(), user_2_from_db.id.__str__())
            assert friendship.status == 'ACCEPTED', 'Статус != "ACCEPTED"'

    @allure.title('Отклонение запроса на дружбу')
    def test_decline_invitation(self, soap_session, auth_client):
        user_1, user_2 = fake.name(), fake.name()
        with allure.step(f'Создать пользователей {user_1} и {user_2} в системе'):
            auth_client.register(user_1, fake.password(special_chars=False))
            auth_client.register(user_2, fake.password(special_chars=False))
            db_client = UsersDb(USER_DB_URL)
            user_1_from_db = db_client.get_user(user_1)
            user_2_from_db =  db_client.get_user(user_2)

        with allure.step(f'Отправить запрос на дружбу от {user_1} к {user_2}'):
            soap_session.request(data=send_invitation_xml(user_1, user_2))

        with allure.step('Убедиться, что статус приглашения в БД == PENDING'):
            friendship = db_client.get_friendship(user_1_from_db.id.__str__(), user_2_from_db.id.__str__())
            assert friendship.status == 'PENDING', 'Статус != "PENDING"'

        with allure.step(f'Отклонить запрос на дружбу пользователем {user_2} от {user_1}'):
            soap_session.request(data=decline_invitation_xml(user_2, friend=user_1))

        with allure.step('Убедиться в отсутствии записи о дружбе в БД'):
            friendship = db_client.get_friendship(user_1_from_db.id.__str__(), user_2_from_db.id.__str__())
            assert not friendship, 'Есть запись о дружбе в БД'