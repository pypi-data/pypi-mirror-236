from datetime import datetime

from app.wrapper_kafka.event_types import (HandlerID, IsoFormatDatetime, URI, AvailableForProcessing,
                                           SfCommentRequest, AwaitingDownload, ParquetsAvailable,
                                           VMCParquetAvailable)
from app.wrapper_kafka.event_types import KafkaEvent


def process_event(event: KafkaEvent, arg1, arg2):
    print(f'processing: {event} with args: {arg1}, {arg2}')


ev_handler = HandlerID()
ev_uri = URI('/tmp/bundle01234567.zip')
ev_case_number = '01234567'
ev_text = 'test text'
ev_size = 12345
parquet_file_names = ['/tmp/parq1.parquet', '/tmp/parq2.parquet']
ev_product_name = 'VBR'
ev_rule_names = ['rule1', 'rule2']
ev_type = "KafkaEvent"

base_event = KafkaEvent(
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat()),
    type=ev_type
)

available_for_processing_event = AvailableForProcessing(
    uri=ev_uri,
    size=ev_size,
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat())
)

download_event = AwaitingDownload(
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat()),
    uri=ev_uri, size=100
)

comment_request_event = SfCommentRequest(
    case_number=ev_case_number,
    text=ev_text,
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat())
)

parquets_available_event = ParquetsAvailable(
    uri=ev_uri,
    size=ev_size,
    file_names=parquet_file_names,
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat())
)

vmc_parquet_available_event = VMCParquetAvailable(
    file_names=parquet_file_names,
    product_name=ev_product_name,
    rule_names=ev_rule_names,
    handler_id=ev_handler,
    last_modified=IsoFormatDatetime(datetime.now().isoformat())
)
