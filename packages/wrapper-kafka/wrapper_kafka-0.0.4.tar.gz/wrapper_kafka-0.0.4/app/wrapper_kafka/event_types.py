import os
from typing import List, NewType

from pydantic import BaseModel

# Kafka event default fields
IsoFormatDatetime = NewType('IsoFormatDatetime', str)
URI = NewType("URI", str)


class HandlerID(BaseModel):
    """ call this with empty parens to get dynamic defaults (unsafe)
    """
    node_name: str = os.uname().nodename
    pid: int = os.getpid()


# Base:
class KafkaEvent(BaseModel):
    """Base event class with properties common to all events"""
    handler_id: HandlerID
    last_modified: IsoFormatDatetime
    type: str


# Downloader events:
class AwaitingDownload(KafkaEvent):
    """Event indicating a bundle that available for download"""
    uri: URI
    size: int
    type: str = "AwaitingDownload"


class AvailableForProcessing(KafkaEvent):
    """Event indicating an uri that is reachable and available for processing"""
    uri: URI
    size: int
    type: str = "AvailableForProcessing"


# VMC Extractor events:
class VMCZipAvailable(KafkaEvent):
    # Renamed ForeignAvailableForProcessing
    """Event indicating a VMC mini zip that is reachable
     and available for processing"""
    uri: URI
    size: int
    region: str
    type: str = "ForeignAvailableForProcessing"


# VMC Enricher events:
class VMCParquetAvailable(KafkaEvent):
    """Event indicating that vmc zip has been processed
       and new VMC parquets are available for analysis"""
    file_names: List[str]
    product_name: str
    rule_names: List[str]
    type: str = "VMCParquetAvailable"


# SF commenter events:
class SfCommentRequest(KafkaEvent):
    case_number: str
    text: str
    type: str = "SfCommentRequest"


# Log parser events:
class ParserRulesUpdate(KafkaEvent):
    value: str
    type: str = "ParserRulesUpdate"


# Logs enricher events:
class ParquetsAvailable(KafkaEvent):
    # Renamed AvailableForAnalysis
    """Event indicating an uri that has been processed and parquets
     are available for analysis"""
    uri: URI
    size: int
    file_names: List[str]
    type: str = "ParquetsAvailable"

    def __str__(self):
        return f"ParquetsAvailable(" \
               f"uri={self.uri}, " \
               f"last_modified={self.last_modified})"


# Stacktrace Aggregation events:
class StackTrace(BaseModel):
    lines: str
    log_name: str
    product_version: str


class StacktraceFound(KafkaEvent):
    uri: URI
    pq_name: str
    group: str
    stacktraces: List[StackTrace]
    last_modified: IsoFormatDatetime
    type: str = "StacktraceFound"

    def __str__(self):
        return f"StacktraceFound(" \
               f"uri={self.uri}, " \
               f"group={self.group}, " \
               f"file_name={self.pq_name}, " \
               f"last_modified={self.last_modified})"


class AggregationDataUpdated(KafkaEvent):
    new_keys: List[int]
    last_modified: IsoFormatDatetime
    type: str = "AggregationDataUpdated"
