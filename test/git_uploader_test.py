"""This module contains tests for the giet_service module"""
import asyncio
from typing import Callable, Iterable
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from aiohttp.tracing import TraceRequestEndParams
from dotenv import load_dotenv

import context
from git_uploader import GitStatitisicsUploader
from rest_objects import ServicStatus

load_dotenv('.env')


def run(callable: Callable, args: Iterable):
    return asyncio.run(callable(args))


class GitStatitisicsUploaderShould(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.git_uploader = GitStatitisicsUploader()

    def test_returns_404_when_invalid_git_user_request(self):
        res = run(self.git_uploader.get_statistics, ('fake_user12321??1as'))
        self.assertEqual(res.http_code, 404)
        self.assertEqual(res.status, ServicStatus.FAILED)

    @patch('kafka_handler.publish')
    def test_returns_500_when_valid_request_but_not_published_on_kafka(self, mock_kafka):
        mock_kafka.return_value.is_done = False
        res = run(self.git_uploader.get_statistics, ('jamesrea97'))
        self.assertEqual(res.http_code, 500)
        self.assertEqual(res.status, ServicStatus.FAILED)

    @patch('kafka_handler.publish')
    def test_return_200_when_valid_request_and_published_on_kafka(self, mock_kafka):
        mock_kafka.return_value.is_done = True
        mock_kafka.return_value.exception = None
        res = run(self.git_uploader.get_statistics, ('jamesrea97'))
        self.assertEqual(res.http_code, 200)
        self.assertEqual(res.status, ServicStatus.PUBLISHED)


if __name__ == "__main__":

    unittest.main()
