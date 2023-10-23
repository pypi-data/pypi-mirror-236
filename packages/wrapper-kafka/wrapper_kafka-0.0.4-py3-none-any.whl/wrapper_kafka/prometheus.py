from typing import Optional, Tuple, List

from prometheus_client import start_http_server, Counter


def start_prometheus_server(metrics_port, logger) -> Optional[bool]:
    try:
        logger.info(f'starting prometheus monitoring at port '
                    f'{metrics_port}')
        start_http_server(port=metrics_port)
        return True
    except Exception as ex:
        logger.consumer_exception(f'monitoring server exception: {ex}')
        raise ex


def create_custom_counters(counters: List[Tuple[str, str]]) -> List[Counter]:
    return [Counter(*pair) for pair in counters]


def declare_basic_kafka_consumer_metrics() -> Tuple[Counter, Counter, Counter]:
    inspected, wrong_message, consumer_exception = create_custom_counters(
        [
            ("inspected_messages", "--> Total messages received from kafka "
                                   "for evaluation."),
            ("wrong_message", "--> Total number of inspected messaged "
                              "with unexpected event type"),
            ("consumer_exceptions", "--> Number of default exceptions thrown "
                                    "on event processing by consumer"),
        ]
    )
    return inspected, wrong_message, consumer_exception
