"""This module contains the main driver of the service"""
import os
import logging

from rest_interface import app
from dotenv import load_dotenv

load_dotenv('.env')


def setup_logging():
    log_level = os.getenv('LOGGING_LEVEL', logging.INFO)
    logging.basicConfig(
        filename='service.log',
        filemode='a',
        level=log_level,
        format='%(asctime)s git-sanitizer %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')


def main():
    setup_logging()

    app.run()


if __name__ == "__main__":
    main()
