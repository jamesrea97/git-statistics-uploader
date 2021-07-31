"""Module contains dataclass objects for service"""
from dataclasses import dataclass
from uuid import uuid4
from typing import Optional
import datetime
import json
from enum import Enum
import uuid


class ServicStatus(Enum):
    PUBLISHED = 'PUBLISHED'
    FAILED = 'FAILED'

class ConnectionStatus(Enum):
    OK = "OK"
    FAILED = "FAILED"


@dataclass
class GitUploadedEvent:
    id_: uuid4
    topic: str
    timestamp: datetime
    load: dict[str, str]

    def __init__(self,
                 id_: uuid4,
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


@dataclass
class GitUploadedResponse:
    http_code: int
    status: ServicStatus
    id_: Optional[uuid4] = None
    parameter: Optional[str] = None

    def to_json(self):
        return {
            "http_code": self.http_code,
            "status": self.status,
            "id_": str(self.id_),
            "parameter": self.parameter
        }


@dataclass
class KafkaConnection:
    server: str
    topic: str
    partition_count: int
    connection_status: ConnectionStatus

    def to_json(self):
        return {
            "server": self.server,
            "topic": self.topic,
            "partition_count": self.partition_count,
            "connection_status": str(self.connection_status)
        }


@dataclass
class GithubConnection:
    base_url: str
    connection_status: ConnectionStatus

    def to_json(self):
        return {
            "base_url": self.base_url,
            "connection_status": str(self.connection_status)
        }


@dataclass
class GitUploadedHealthResponse:
    id_: uuid4
    timestamp: datetime
    kafka_connection: KafkaConnection
    github_connection: GithubConnection

    def to_json(self):
        return {
            "id_": str(self.id_),
            "timestamp": str(self.timestamp),
            "kafka_connection": self.kafka_connection.to_json(),
            "github_connection": self.github_connection.to_json()

        }
