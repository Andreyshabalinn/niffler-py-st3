import json

from allure import step, epic, suite, title, id, tag
from faker import Faker

from tests.models.user import UserName


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