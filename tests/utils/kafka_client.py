import json
import logging
from typing import Sequence

from tests.models.user import UserName
from confluent_kafka import TopicPartition
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, Consumer, Producer

from tests.utils.waiters import wait_until_timeout

class KafkaClient:
    """Класс для взаимодействия с кафкой"""

    def __init__(
            self,
            server_name,
            client_id: str = 'tester',
            group_id: str = 'tester',

    ):
        self.server = server_name
        self.admin = AdminClient(
            {"bootstrap.servers": f"{self.server}:9092"}
        )
        self.producer = Producer(
            {"bootstrap.servers": f"{self.server}:9092"}
        )
        self.consumer = Consumer(
            {
                "bootstrap.servers": f"localhost:9092",
                "group.id": group_id,
                "client.id": client_id,
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
                "enable.ssl.certificate.verification": False
            }
        )
        md = self.consumer.list_topics(timeout=5)
        print("Список топиков:")
        for t in md.topics.keys():
            print(" -", t)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()
        self.producer.flush()

    def list_topics_names(self, attempts: int = 5):
        """Вернуть список доступных топиков"""
        try:
            topics = self.admin.list_topics(timeout=attempts).topics
            return [topics.get(item).topic for item in topics]
        except RuntimeError:
            logging.error("no topics in kafka")

    @wait_until_timeout
    def consume_message(self, partitions, **kwargs):
        """Вернуть последнее после определенной позиции сообщение"""
        self.consumer.assign(partitions)
        try:
            message = self.consumer.poll(1.0)
            logging.debug(f'{message.value()}')
            return message.value()
        except AttributeError:
            pass

    def get_last_offset(self, topic: str = "", partition_id=0):
        """Вернуть последнюю позицию партиции"""
        partition = TopicPartition(topic, partition_id)
        try:
            low, high = self.consumer.get_watermark_offsets(partition, timeout=10)
            return high
        except Exception as err:
            logging.error("probably no such topic: %s: %s", topic, err)

    def log_msg_and_json(self, topic_partitions):
        msg = self.consume_message(topic_partitions, timeout=25)
        logging.info(msg)
        return msg

    def subscribe_listen_new_offsets(self, topic):
        self.consumer.subscribe([topic])
        p_ids = self.consumer.list_topics(topic).topics[topic].partitions.keys()
        partitions_offsets_event = {k: self.get_last_offset(topic, k) for k in p_ids}
        logging.info(f'{topic} offsets: {partitions_offsets_event}')
        topic_partitions = [TopicPartition(topic, k, v) for k, v in partitions_offsets_event.items()]
        return topic_partitions

    def delivery_report(self, err, msg):
        if err is not None:
            logging.info(f"Ошибка при отправке сообщения: {err}")
        else:
            print(f"Сообщение отправлено в {msg.topic()} [{msg.partition()}] с смещением {msg.offset()}")

    def send_message(self, topic: str, username: str):
        self.producer.produce(topic,
                              json.dumps(UserName(username=username).model_dump()).encode("utf-8"),
                              on_delivery=self.delivery_report,
                              headers={"__TypeId__": "guru.qa.niffler.model.UserJson"},
                              )
        self.producer.flush()