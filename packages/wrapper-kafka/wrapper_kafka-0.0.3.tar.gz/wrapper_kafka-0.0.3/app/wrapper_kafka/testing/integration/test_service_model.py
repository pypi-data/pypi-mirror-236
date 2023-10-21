import operator
from unittest import TestCase

from app.wrapper_kafka.data_types import KafkaProducerSettings, KafkaConsumerSettings
from app.wrapper_kafka.event_types import (AvailableForProcessing,
                                           SfCommentRequest, AwaitingDownload, ParquetsAvailable,
                                           VMCParquetAvailable)
from app.wrapper_kafka.kafka_consumer import MessageConsumer
from app.wrapper_kafka.kafka_producer import MessageProducer
from app.wrapper_kafka.logger import get_default_logger
from app.wrapper_kafka.testing import (vmc_parquet_available_event,
                                       available_for_processing_event, parquets_available_event,
                                       comment_request_event, download_event)


class TestServiceModelIntegration(TestCase):
    def setUp(self) -> None:
        self.kafka_nodes = ['localhost:9092']
        self.producer_settings = KafkaProducerSettings(
            kafka_nodes=self.kafka_nodes,
            kafka_topic='test'
        )
        self.kafka_producer = MessageProducer(self.producer_settings)
        self.consumer_settings = KafkaConsumerSettings(
            event_types=[AvailableForProcessing,
                         SfCommentRequest,
                         ParquetsAvailable,
                         AwaitingDownload,
                         VMCParquetAvailable],
            topic_names=['test'],
            kafka_nodes=self.kafka_nodes,
            group_name='kafka_poc1',
            strategy='earliest')
        self.consumer_timeout_sec = 15

        self.message_consumer = MessageConsumer(
            consumer_settings=self.consumer_settings,
            consumer_timeout_sec=self.consumer_timeout_sec
        )

        self.logger = get_default_logger()
        self.events_list = [available_for_processing_event,
                            download_event,
                            comment_request_event,
                            parquets_available_event,
                            vmc_parquet_available_event]

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
