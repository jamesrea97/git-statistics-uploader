"""This module contains the main driver of the service"""
from rest_interface import app
from dotenv import load_dotenv

load_dotenv('.env')


def main():

    # TODO set up logs here
    app.run()


if __name__ == "__main__":
    main()
