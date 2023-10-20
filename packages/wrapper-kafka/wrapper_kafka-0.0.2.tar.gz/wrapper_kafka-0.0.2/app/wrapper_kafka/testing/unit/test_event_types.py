from unittest import TestCase

from app.wrapper_kafka.event_types import (HandlerID, IsoFormatDatetime, URI, KafkaEvent,
                                           AwaitingDownload, SfCommentRequest, ParquetsAvailable)
from app.wrapper_kafka.logger import get_default_logger


class EventsTest(TestCase):

    def setUp(self) -> None:
        self.ev_handler = HandlerID()
        self.ev_time = IsoFormatDatetime('2023-08-30T13:44:11.300929')
        self.ev_uri = URI('/tmp/bundle01234567.zip')
        self.ev_case_number = '01234567'
        self.ev_text = 'test text'
        self.logger = get_default_logger()
        self.ev_size = 12345
        self.parquet_file_name = ['/tmp/parq1.parquet', '/tmp/parq2.parquet']

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

        self.all_events = [self.download_event,
                           self.comment_request_event,
                           self.parquets_available_event]

    def test_create_all_event_types(self):
        for ev in self.all_events:
            self.logger.info(f'constructed: {ev}')
            self.assertIsInstance(ev, KafkaEvent)
