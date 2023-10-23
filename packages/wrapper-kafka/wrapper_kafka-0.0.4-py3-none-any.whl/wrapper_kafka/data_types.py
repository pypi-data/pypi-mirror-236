from typing import List, Optional, Type

from pydantic import BaseModel

from .event_types import KafkaEvent


# Base data types
class KafkaConsumerSettings(BaseModel):
    event_types: List[Type[KafkaEvent]]
    topic_names: List[str]
    kafka_nodes: List[str]
    group_name: Optional[str]
    strategy: str


class KafkaProducerSettings(BaseModel):
    kafka_nodes: List[str]
    kafka_topic: str
