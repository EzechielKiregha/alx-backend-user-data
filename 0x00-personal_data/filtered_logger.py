#!/usr/bin/env python3
"""
this is a function that returns
a log on the screen
"""
from typing import List
import logging
import re
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    for item in fields:
        message = re.sub(rf"{item}=(.*?)\{separator}",
                         f"{item}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    this is method returns a
    logging.Logger()
    object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel = logging.INFO
    logger.propagate = False
    formater = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler = logging.StreamHandler(formater)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    is a function that returns a mysql connection
    to a particular server with the mentionned credentials
    """
    user_name = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host_name = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(host=host_name,
                                         user=user_name,
                                         password=passwd, database=db_name)
    return connection
