"""This module contains GitService logic"""
import uuid
import os
from datetime import datetime
import logging
from urllib.parse import urljoin

import http_request as http_request
import kafka_handler as kafka_handler

from domain_objects import (
    ConnectionStatus,
    GithubConnection,
    KafkaConnection,
    ServicStatus,
    GitUploadedResponse,
    GitUploadedEvent,
    GitUploadedHealthResponse
)


class GitStatitisicsUploader:
    def __init__(self):
        self.git_url = os.getenv("GIT_BASE_URL")
        self.kafka_endpoint = os.getenv("KAFKA_ENDPOINT")
        self.kafka_repo_consumer_topic = os.getenv("KAFKA_REPO_CONSUMER_TOPIC")
        self.kafka_repo_consumer_group = os.getenv("KAFKA_REPO_CONSUMER_GROUP")
        self.kafka_repo_producer_topic = os.getenv("KAFKA_REPO_PRODUCER_TOPIC")

    async def upload_user(self, git_user: str) -> GitUploadedResponse:
        # TODO handle different git events

        repo = f'users/{git_user}/repos'

        url = urljoin(base=self.git_url, url=repo)

        res = await http_request.get(url)

        if res.status == 200:
            logging.info(f"Successfully retrieved data for user: {git_user} from GitHub.")
            event = GitUploadedEvent(id_=uuid.uuid4(),
                                     timestamp=datetime.utcnow(),
                                     topic=self.kafka_repo_producer_topic,
                                     str_load=res.response)

            kafka_res = await kafka_handler.publish(self.kafka_endpoint,
                                                    self.kafka_repo_producer_topic,
                                                    event.to_json())

            if kafka_res.exception is None and kafka_res.is_done:
                logging.info(f"Successfully published event with id: {event.id_} to Kafka.")

                return GitUploadedResponse(http_code=200,
                                           status=ServicStatus.PUBLISHED,
                                           id_=event.id_,
                                           parameter=git_user)
            else:
                logging.warning(f"Failed to published event with id: {event.id_} to Kafka.")
                return GitUploadedResponse(http_code=500,
                                           status=ServicStatus.FAILED,
                                           id_=event.id_,
                                           parameter=git_user)
        else:
            logging.warning(f"Failed to retrieved data for user: {git_user} from GitHub.")
            return GitUploadedResponse(http_code=404,
                                       status=ServicStatus.FAILED,
                                       id_=None,
                                       parameter=git_user)

    async def get_health(self):

        github_check = await self.__test_github_connection()

        kafka_check = await self.__test_kafka_connection()

        return GitUploadedHealthResponse(id_=uuid.uuid4(),
                                         timestamp=datetime.utcnow(),
                                         kafka_connection=kafka_check,
                                         github_connection=github_check
                                         )

    async def __test_github_connection(self) -> GithubConnection:
        url = urljoin(base=self.git_url, url='users/python/repos')
        res = await http_request.get(url)

        return GithubConnection(base_url=self.git_url,
                                connection_status=ConnectionStatus.OK
                                if res.status == 200
                                else ConnectionStatus.FAILED)

    async def __test_kafka_connection(self) -> KafkaConnection:
        kafka_res = await kafka_handler.get_partitions(self.kafka_endpoint,
                                                       self.kafka_repo_producer_topic)

        return KafkaConnection(server=self.kafka_endpoint,
                               topic=self.kafka_repo_producer_topic,
                               partition_count=len(kafka_res) if kafka_res else None,
                               connection_status=ConnectionStatus.OK
                               if kafka_res
                               else ConnectionStatus.FAILED)
