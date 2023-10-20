import operator
from unittest import TestCase

from app.wrapper_kafka.data_types import KafkaProducerSettings, KafkaConsumerSettings
from app.wrapper_kafka.event_types import (HandlerID, IsoFormatDatetime, URI, AvailableForProcessing,
                                           SfCommentRequest, AwaitingDownload, ParquetsAvailable)
from app.wrapper_kafka.kafka_consumer import MessageConsumer
from app.wrapper_kafka.kafka_producer import MessageProducer
from app.wrapper_kafka.logger import get_default_logger


class TestServiceModelIntegration(TestCase):
    def setUp(self) -> None:
        self.kafka_nodes = ['localhost:9092']
        self.producer_settings = KafkaProducerSettings(
            kafka_nodes=self.kafka_nodes,
            kafka_topic='test'
        )
        self.kafka_producer = MessageProducer(self.producer_settings)
        self.consumer_settings = KafkaConsumerSettings(
            event_types=[AvailableForProcessing, SfCommentRequest, ParquetsAvailable, AwaitingDownload],
            topic_names=['test'],
            kafka_nodes=self.kafka_nodes,
            group_name='kafka_poc1',
            strategy='earliest')
        self.consumer_timeout_sec = 15

        self.message_consumer = MessageConsumer(
            consumer_settings=self.consumer_settings,
            consumer_timeout_sec=self.consumer_timeout_sec
        )

        self.ev_handler = HandlerID()
        self.ev_time = IsoFormatDatetime('2023-08-30T13:44:11.300929')
        self.ev_uri = URI('/tmp/bundle01234567.zip')
        self.ev_case_number = '01234567'
        self.ev_text = 'test text'
        self.logger = get_default_logger()
        self.ev_size = 12345
        self.parquet_file_name = ['/tmp/parq1.parquet', '/tmp/parq2.parquet']

        self.available_for_processing_event = AvailableForProcessing(
            uri=self.ev_uri,
            size=self.ev_size,
            handler_id=self.ev_handler,
            last_modified=self.ev_time
        )

        self.download_event = AwaitingDownload(
            handler_id=self.ev_handler,
            last_modified=self.ev_time,
            uri=self.ev_uri, size=100
        )

        self.comment_request_event = SfCommentRequest(
            case_number=self.ev_case_number,
            text=self.ev_text,
            handler_id=self.ev_handler,
            last_modified=self.ev_time
        )

        self.parquets_available_event = ParquetsAvailable(
            uri=self.ev_uri,
            size=self.ev_size,
            file_names=self.parquet_file_name,
            handler_id=self.ev_handler,
            last_modified=self.ev_time
        )
        self.events_list = [self.available_for_processing_event,
                            self.download_event,
                            self.comment_request_event,
                            self.parquets_available_event]

    def test_sending_and_reading_kafka_messages(self):
        self.consumed_messages = []
        for ev in self.events_list:
            self.kafka_producer.send_message(kafka_message=ev)

        for msg in self.message_consumer.consume_messages():
            self.logger.info(f'consumed: {msg}')
            self.consumed_messages.append(msg)

        self.assertEqual(len(self.consumed_messages), len(self.events_list))
        self.assertEqual(sorted(self.consumed_messages, key=operator.attrgetter('last_modified')),
                         sorted(self.events_list, key=operator.attrgetter('last_modified')))
