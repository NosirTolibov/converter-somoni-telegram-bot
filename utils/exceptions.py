"""
Custom exception thrown by the application
"""
import logging
from requests.exceptions import (HTTPError, RequestException, Timeout, ConnectionError)

logger = logging.getLogger()


class NotCorrectMessage(Exception):
    """Invalid message that could not be parsed"""
    # logger.info(f'Bot can not parse input text')


class ApiResponseException(Exception):
    """Catches API request exception"""
    def __init__(self, exception: Exception):
        if isinstance(exception, HTTPError):
            logger.error(f'HTTPError: {exception}')
        if isinstance(exception, RequestException):
            logger.error(f'RequestException: {exception}')
        if isinstance(exception, Timeout):
            logger.error(f'Timeout: {exception}')
        if isinstance(exception, ConnectionError):
            logger.error(f'ConnectionError: {exception}')
        else:
            logger.error(f'Something went wrong: {exception}')

