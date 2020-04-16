import logging

import psycopg2

import weather_bot.settings as settings


logger = logging.getLogger(__name__)


class Database(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                logger.info('Connecting to Database...')
                connection = Database._instance.connection = psycopg2.connect(**settings.DB_CONF)
                Database._instance.cursor = connection.cursor()
            except Exception as e:
                logger.warning(f'Error {e} occured while establishing connection to Database')
                Database._instance = None
        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def exec(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.warning(f'Error {e} occured while executing query {query}')

    def fetch(self):
        return self.cursor.fetchall()

    def exec_and_fetch(self, query):
        self.exec(query)
        return self.fetch()

    def __del__(self):
        self.connection.close()
        self.cursor.close()
