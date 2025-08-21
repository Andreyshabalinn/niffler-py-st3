import json
import logging

from allure import step, epic, suite, title, id, tag
from faker import Faker
from tests.config import USER_DB_URL

from tests.models.user import UserName
from tests.database.user_db import UsersDb


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@suite("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
class TestAuthRegistrationKafkaTest:
        @id("600001")
        @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
        @tag("KAFKA")
        def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka):
                username = Faker().user_name()
                password = Faker().password(special_chars=False)

                topic_partitions = kafka.subscribe_listen_new_offsets("users")

                result = auth_client.register(username, password)
                assert result.status_code == 201

                event = kafka.log_msg_and_json(topic_partitions)

                with step("Check that message from kafka exist"):
                        assert event != '' and event != b''

                with step("Check message content"):
                        UserName.model_validate(json.loads(event.decode('utf8')))
                        assert json.loads(event.decode('utf8'))['username'] == username

        @title('Сервис niffler-userdata должен забирать сообщение из топика Kafka')
        def test_niffler_userdata_should_consume_message_from_kafka(self, kafka):
                with step('Отправить сообщение в Kafka'):
                        user_name_for_msg = Faker().user_name()
                        logging.info(f'Отправить сообщение по пользователю: {user_name_for_msg}')
                        kafka.send_message("users", user_name_for_msg)
                        
                with step('Убедиться, что в таблице userdata есть запись о пользователе из сообщения'):
                        db_client = UsersDb(USER_DB_URL)
                        user_from_db = db_client.get_user(username=user_name_for_msg)
                        assert user_from_db.username == user_name_for_msg