from kafka import KafkaProducer

from .data_types import KafkaProducerSettings
from .event_types import KafkaEvent
from .logger import get_default_logger


class MessageProducer:
    def __init__(self,
                 producer_settings: KafkaProducerSettings):
        self.logger = get_default_logger()
        self.producer_settings = producer_settings
        self.producer = self.create_producer()

    def serialize_event(self, event: KafkaEvent) -> bytes:
        try:
            json_event = event.model_dump_json()
            return json_event.encode(encoding="utf-8", errors="replace")
        except Exception as ex:
            self.logger.exception(ex)

    def create_producer(self) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=self.producer_settings.kafka_nodes,
            acks=1,
            value_serializer=self.serialize_event,
            max_in_flight_requests_per_connection=1,
            max_request_size=10485760,
            buffer_memory=33554432,
            retry_backoff_ms=2000
        )

    def send_message(self, kafka_message: KafkaEvent):
        try:
            self.logger.info(f'sending kafka message: {kafka_message}')
            self.producer.send(topic=self.producer_settings.kafka_topic,
                               value=kafka_message)
            self.producer.flush()
        except Exception as ex:
            self.logger.exception(f'exception on sending kafka message: {ex}')
