#!/usr/bin/env python3
"""
this module contains user data management
"""
from typing import List
import logging
import mysql.connector
import os
import re


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    this function returns the log message obfuscated - the function uses
    a regex to replace occurences of certain field values
    """
    for field in fields:
        replace = "{}={}{}".format(field, redaction, separator)
        message = re.sub("{}=.*?{}".format(field, separator), replace, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialization method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """this function filters values in incoming log records using
         filter_datum function"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """this method returns a user data logger"""
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(stream_handler)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db function that returns a connector to the database"""
    db_connection = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'))
    return db_connection


def main() -> None:
    """function will obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under a filtered format
    """
    my_db = get_db()
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()

    log = get_logger()

    for row in data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        log.info(fields)
    cursor.close()
    my_db.close()


if __name__ == "__main__":
    main()
