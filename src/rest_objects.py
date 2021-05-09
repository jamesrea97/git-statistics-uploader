"""This module contains REST interface objects"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ServicStatus:
    PUBLISHED = 'PUBLISHED'
    FAILED = 'FAILED'


@dataclass
class ServiceResponse:
    http_code: int
    status: ServicStatus
    id_: Optional[UUID] = None
    parameter: Optional[str] = None

    def to_json(self):
        return {
            "http_code": self.http_code,
            "status": self.status,
            "id_": str(self.id_),
            "parameter": self.parameter
        }
