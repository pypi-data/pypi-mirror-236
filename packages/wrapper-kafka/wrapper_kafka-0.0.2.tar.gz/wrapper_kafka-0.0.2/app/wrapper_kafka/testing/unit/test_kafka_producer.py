from unittest import TestCase, mock

from app.wrapper_kafka.data_types import KafkaProducerSettings
from app.wrapper_kafka.event_types import KafkaEvent, HandlerID, IsoFormatDatetime
from app.wrapper_kafka.kafka_producer import MessageProducer


class TestWrappersKafkaProducer(TestCase):

    @mock.patch('app.wrapper_kafka.kafka_producer.KafkaProducer',
                autospec=True)
    def setUp(self, producer_mock) -> None:
        self.ev_handler = HandlerID()
        self.ev_time = IsoFormatDatetime('2023-08-30T13:44:11.300929')
        self.ev_type = "KafkaEvent"
        self.producer_settings = KafkaProducerSettings(
            kafka_nodes=['node1:9092', 'node2:9092'],
            kafka_topic='test'
        )
        self.kafka_producer = MessageProducer(producer_settings=self.producer_settings)
        self.event = KafkaEvent(handler_id=self.ev_handler,
                                last_modified=self.ev_time,
                                type=self.ev_type)
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
