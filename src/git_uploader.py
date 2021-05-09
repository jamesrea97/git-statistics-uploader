"""This module contains GitService logic"""
import uuid
import os
from datetime import datetime
import logging
from urllib.parse import urljoin

import http_request as http_request
import kafka_handler as kafka_handler
from event_objects import ServicStatus, ServiceResponse, Event


class GitStatitisicsUploader:
    def __init__(self):
        self.git_url = os.getenv("GIT_BASE_URL")
        self.kafka_endpoint = os.getenv("KAFKA_ENDPOINT")
        self.kafka_repo_uploaded_topic = os.getenv("KAFKA_REPO_UPLOADED_TOPIC")

    async def get_statistics(self, git_user: str) -> ServiceResponse:
        # TODO handle different git events

        repo = f'users/{git_user}/repos'

        url = urljoin(base=self.git_url, url=repo)

        res = await http_request.get(url)

        if res.status == 200:
            event = Event(id_=uuid.uuid4(),
                                 timestamp=datetime.utcnow(),
                                 topic=self.kafka_repo_uploaded_topic,
                                 str_load=res.response)

            kafka_res = await kafka_handler.publish(self.kafka_endpoint,
                                                    self.kafka_repo_uploaded_topic,
                                                    event.to_json())

            if kafka_res.exception is None and kafka_res.is_done:
                return ServiceResponse(http_code=200,
                                       status=ServicStatus.PUBLISHED,
                                       id_=event.id_,
                                       parameter=git_user)
            else:
                return ServiceResponse(http_code=500,
                                       status=ServicStatus.FAILED,
                                       id_=event.id_,
                                       parameter=git_user)
        else:
            return ServiceResponse(http_code=404,
                                   status=ServicStatus.FAILED,
                                   id_=None,
                                   parameter=git_user)


# TODO health system of the kafka queue and git website
