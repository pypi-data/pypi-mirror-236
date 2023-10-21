import json
from threading import Thread
from time import sleep

from kafka import KafkaConsumer

from .data_types import KafkaConsumerSettings
from .event_types import KafkaEvent
from .logger import get_default_logger
from .prometheus import start_prometheus_server, declare_basic_kafka_consumer_metrics


class MessageConsumer:
    def __init__(self,
                 consumer_settings: KafkaConsumerSettings,
                 consumer_auto_commit: bool = False,
                 max_poll_interval_sec: int = 600,
                 heartbeat_logging_interval_sec: int = 600,
                 metrics_port: int = 8000,
                 consumer_timeout_sec: int = float('inf'),
                 max_poll_records: int = 1):

        self.consumer_timeout_ms = consumer_timeout_sec * 1000
        self.max_poll_records = max_poll_records
        self.metrics_port = metrics_port
        self.logger = get_default_logger()
        self.consumer_settings = consumer_settings
        self.consumer_auto_commit = consumer_auto_commit
        self.max_poll_interval = max_poll_interval_sec * 1000
        # request_timeout_error has to be > max_poll_interval
        self.request_timeout_ms = self.max_poll_interval + 5000
        # connections_max_idle_ms has to be > request_timeout_error
        self.connections_max_idle_ms = self.request_timeout_ms + 10000
        self.events_mapper = {ev.__name__: ev for ev in consumer_settings.event_types}
        self.consumer = self.create_consumer()
        self.heartbeat_logging_interval = heartbeat_logging_interval_sec
        self.monitoring_thread = Thread(target=self.initialize_monitoring, daemon=True)
        self.monitoring_thread.start()
        self.inspected, self.wrong_message, self.consumer_exception = declare_basic_kafka_consumer_metrics()

    def start_heartbeat(self):
        while True:
            sleep(self.heartbeat_logging_interval)
            self.logger.info('♥-❤-♥ heartbeat ❤-♥-❤')

    def initialize_monitoring(self):
        start_prometheus_server(metrics_port=self.metrics_port, logger=self.logger)
        self.start_heartbeat()

    def deserialize_event(self, msg_value: bytes) -> KafkaEvent:
        try:
            message = json.loads(msg_value)
            message_ev_type = message['type']
            if message_ev_type in self.events_mapper.keys():
                event_type = self.events_mapper[message_ev_type]
                return event_type(**message)
            else:
                self.wrong_message.inc(1)
                self.logger.warning(f'{message_ev_type} '
                                    f'is out of the expected events scope, skipping')
                # TODO: cast unknown event types to a default(typeless) kafka event?
        except Exception as ex:
            self.consumer_exception.inc(1)
            self.logger.exception(f'message deserialization exception: {ex}')

    def create_consumer(self) -> KafkaConsumer:
        consumer = KafkaConsumer(
            group_id=self.consumer_settings.group_name,
            bootstrap_servers=self.consumer_settings.kafka_nodes,
            auto_offset_reset=self.consumer_settings.strategy,
            value_deserializer=self.deserialize_event,
            session_timeout_ms=30000,
            request_timeout_ms=self.request_timeout_ms,
            enable_auto_commit=self.consumer_auto_commit,
            max_poll_records=self.max_poll_records,
            connections_max_idle_ms=self.connections_max_idle_ms,
            max_poll_interval_ms=self.max_poll_interval,
            consumer_timeout_ms=self.consumer_timeout_ms
        )
        consumer.subscribe(self.consumer_settings.topic_names)
        self.logger.info(f'subscribed {self.consumer_settings}')

        return consumer

    def consume_messages(self) -> KafkaEvent:
        for message in self.consumer:
            try:
                self.inspected.inc(1)
                event = message.value
                if event:
                    self.logger.info(f'read: {event}')
                    yield event
                else:
                    self.logger.warning(f'consumed message had empty .value: {message}')
            except Exception as ex:
                self.consumer_exception.inc(1)
                self.logger.exception(f'exception on reading kafka message:{ex}')
            finally:
                if not self.consumer_auto_commit:
                    self.consumer.commit()
