from unittest import TestCase

from app.wrapper_kafka.data_types import KafkaProducerSettings, KafkaConsumerSettings, KafkaEvent


class TestDataHelpers(TestCase):

    def setUp(self) -> None:
        self.consumer_topic_names = ['test1', 'test2']
        self.kafka_nodes = ['node1:9092', 'node2:9092']
        self.group_name = 'test_group'
        self.strategy = 'latest'
        self.producer_topic = 'test_producer_topic'

        self.kafka_consumer_settings = KafkaConsumerSettings(
            event_types=[KafkaEvent],
            topic_names=self.consumer_topic_names,
            kafka_nodes=self.kafka_nodes,
            group_name=self.group_name,
            strategy=self.strategy
        )
        self.kafka_producer_settings = KafkaProducerSettings(
            kafka_nodes=self.kafka_nodes,
            kafka_topic=self.producer_topic,
        )

    def test_consumer_settings_repr(self):
        self.assertEqual(repr(self.kafka_consumer_settings),
                         f"KafkaConsumerSettings(event_types=[{str(KafkaEvent)}],"
                         f" topic_names={self.consumer_topic_names},"
                         f" kafka_nodes={self.kafka_nodes},"
                         f" group_name='{self.group_name}',"
                         f" strategy='{self.strategy}')")

    def test_producer_settings_repr(self):
        self.assertEqual(repr(self.kafka_producer_settings),
                         f"KafkaProducerSettings(kafka_nodes={self.kafka_nodes},"
                         f" kafka_topic='{self.producer_topic}')")
