"""Module contains dataclass objects for service"""
from dataclasses import dataclass
import uuid
import typing
import datetime
import json

# Kafka Event
@dataclass
class Event:
    id_: uuid
    topic: str
    timestamp: datetime
    load: dict[str, str]

    def __init__(self,
                 id_: uuid,
                 timestamp: datetime,
                 topic: str,
                 str_load: str):
        self.id_ = id_
        self.topic = topic
        self.timestamp = timestamp
        self.load = json.loads(str_load)

    def to_json(self):
        return {
            "id_": str(self.id_),
            "topic": self.topic,
            "timestamp": str(self.timestamp),
            "load": self.load
        }


# REST Interface
@dataclass
class ServicStatus:
    PUBLISHED = 'PUBLISHED'
    FAILED = 'FAILED'

@dataclass
class ServiceResponse:
    http_code: int
    status: ServicStatus
    id_: typing.Optional[uuid.UUID] = None
    parameter: typing.Optional[str] = None

    def to_json(self):
        return {
            "http_code": self.http_code,
            "status": self.status,
            "id_": str(self.id_),
            "parameter": self.parameter
        }
