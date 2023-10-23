from unittest import TestCase, mock

from app.wrapper_kafka.data_types import KafkaConsumerSettings
from app.wrapper_kafka.event_types import KafkaEvent, HandlerID, IsoFormatDatetime
from app.wrapper_kafka.kafka_consumer import MessageConsumer
from test_wrappers_prometheus import unregister_metrics


class TestWrappersKafkaConsumer(TestCase):

    @mock.patch('app.wrapper_kafka.kafka_consumer.KafkaConsumer',
                autospec=True)
    def setUp(self, consumer_mock) -> None:
        self.ev_handler = HandlerID()
        self.ev_time = IsoFormatDatetime('2023-08-30T13:44:11.300929')
        self.ev_type = "KafkaEvent"

        self.consumer_settings = KafkaConsumerSettings(
            event_types=[KafkaEvent], topic_names=['test'],
            kafka_nodes=['node1:9092', 'node2:9092'], group_name='kafka_poc1',
            strategy='earliest')
        self.consumer_timeout_sec = 3
        self.kafka_consumer = MessageConsumer(consumer_settings=self.consumer_settings,
                                              consumer_timeout_sec=self.consumer_timeout_sec)
        self.event = KafkaEvent(handler_id=self.ev_handler,
                                last_modified=self.ev_time,
                                type=self.ev_type)
        self.consumer_mock = consumer_mock
        unregister_metrics()

    def tearDown(self) -> None:
        unregister_metrics()

    def test_consume_message_recovers_after_exception(self):
        self.kafka_consumer.logger = mock.MagicMock()
        self.consumer_mock.return_value.__iter__.side_effect = Exception('test exception')
        with self.assertRaises(Exception):
            for _ in self.kafka_consumer.consume_messages():
                pass
