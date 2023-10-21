# wrapper_kafka

Wrapper around python-kafka with pydantic and prometheus-client for easy prod implementation
Kafka event types are made with pydantic BaseModel, create your own event types if required.

## MessageProducer usage

```
from wrapper_kafka import KafkaProducerSettings, MessageProducer
from wrapper_kafka.event_types import AvailableForProcessing, HandlerID, URI, IsoFormatDatetime


def main():
    ev_handler = HandlerID('Test123')
    ev_time = IsoFormatDatetime('2023-08-30T13:44:11.300929')
    ev_uri = URI('/tmp/bundle01234567.zip')
    ev_size = 25569
    test_event = AvailableForProcessing(uri=ev_uri, size=ev_size,
                                        handler_id=ev_handler, last_modified=ev_time)

    producer_settings = KafkaProducerSettings(
        kafka_nodes=['kafka:9002'],
        kafka_topic='test'
    )
    kafka_producer = MessageProducer(producer_settings)
    kafka_producer.send_message(kafka_message=test_event)

if __name__ == "__main__":
    main()

```

## MessageConsumer usage

```
from wrapper_kafka import KafkaConsumerSettings, MessageConsumer, get_default_logger
from wrapper_kafka.event_types import AvailableForProcessing
from functools import partial


def main():
    logger = get_default_logger()
    
    c_settings = KafkaConsumerSettings(
        event_types=[AvailableForProcessing], topic_names=['test'],
        kafka_nodes=['kafka:9092'], group_name='kafka_poc',
        strategy='earliest')

    message_consumer = MessageConsumer(consumer_settings=c_settings)
    for msg in message_consumer.consume_messages():
        logger.info(f'processed: {msg}')
        # do your thing with a message

if __name__ == '__main__':
    main()

```