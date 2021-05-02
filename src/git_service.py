"""This module contains GitService logic"""
import asyncio
import os
import uuid
from datetime import datetime
from dataclasses import dataclass
import logging
import json
from urllib.parse import urljoin

import http_request
import kafka_handler


@dataclass
class RequestEvent:
    id_: uuid
    timestamp: datetime
    request: dict[str, str]

    def to_json(self):
        return {
            "id_": str(self.id_),
            "timestamp": str(self.timestamp),
            "request": self.request
        }


@dataclass
class GitUploadedResponse:
    id_: uuid
    timestamp: datetime
    response: dict[str, str]

    def to_json(self):
        return {
            "id_": str(self.id_),
            "timestamp": str(self.timestamp),
            "response": self.response
        }


class GitStatitisicsUploader:
    def __init__(self):
        self.git_url = "https://api.github.com"
        self.kafka_producer_endpoint = "localhost:9092"
        self.kafka_topic = "git-uploaded"

        # self.git_url = os.getenv('GIT_BASE_URL')
        # TODO add information about the message queue

    async def get_statistics(self, git_user: str) -> GitUploadedResponse:
        repo = f'users/{git_user}/repos'

        url = urljoin(base=self.git_url, url=repo)

        res = await http_request.get(url)

        if res.status == 200:
            json_git_stats = json.loads(res.response)
            kafka_res = await kafka_handler.publish(self.kafka_producer_endpoint,
                                                    self.kafka_topic,
                                                    json_git_stats)
            import pdb
            pdb.set_trace()
            return
        else:
            # TODO
            pass


async def get_health(self):
    pass


g = GitStatitisicsUploader()

t = asyncio.run(g.get_statistics('jamesrea97'))
