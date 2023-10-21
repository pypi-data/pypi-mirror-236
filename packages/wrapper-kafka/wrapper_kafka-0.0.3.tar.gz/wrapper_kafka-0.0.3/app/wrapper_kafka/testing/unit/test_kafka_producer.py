from unittest import TestCase, mock

from app.wrapper_kafka.data_types import KafkaProducerSettings
from app.wrapper_kafka.kafka_producer import MessageProducer
from app.wrapper_kafka.testing import base_event


class TestWrappersKafkaProducer(TestCase):

    @mock.patch('app.wrapper_kafka.kafka_producer.KafkaProducer',
                autospec=True)
    def setUp(self, producer_mock) -> None:

        self.producer_settings = KafkaProducerSettings(
            kafka_nodes=['node1:9092', 'node2:9092'],
            kafka_topic='test'
        )
        self.kafka_producer = MessageProducer(producer_settings=self.producer_settings)
        self.event = base_event
        self.producer_mock = producer_mock

    def test_send_message(self):
        self.kafka_producer.send_message(kafka_message=self.event)
        self.producer_mock.return_value.send.assert_called_once()
        self.producer_mock.return_value.flush.assert_called_once()

    def test_send_message_recovers_after_exception(self):
        self.kafka_producer.logger = mock.MagicMock()
        self.producer_mock.return_value.send.side_effect = Exception('test exception')
        self.kafka_producer.send_message(kafka_message=self.event)
        self.kafka_producer.logger.exception.assert_called_once()
        unpacked_tuple, rest = self.kafka_producer.logger.exception.call_args_list[0]
        logger_message = unpacked_tuple[0]
        self.assertEqual('exception on sending kafka message: test exception', logger_message)
