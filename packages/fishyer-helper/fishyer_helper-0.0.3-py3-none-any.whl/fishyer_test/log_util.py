import logging


class LogUtil:
    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warn(message):
        logging.warn(message)

    @staticmethod
    def error(message):
        logging.error(message)
