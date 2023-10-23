from unittest import TestCase

from app.wrapper_kafka.event_types import (KafkaEvent)
from app.wrapper_kafka.logger import get_default_logger
from app.wrapper_kafka.testing import (vmc_parquet_available_event,
                                       available_for_processing_event, parquets_available_event,
                                       comment_request_event, download_event)


class EventsTest(TestCase):

    def setUp(self) -> None:
        self.logger = get_default_logger()

        self.all_events = [available_for_processing_event,
                           download_event,
                           comment_request_event,
                           parquets_available_event,
                           vmc_parquet_available_event]

    def test_create_all_event_types(self):
        for ev in self.all_events:
            self.logger.info(f'constructed: {ev}')
            self.assertIsInstance(ev, KafkaEvent)
