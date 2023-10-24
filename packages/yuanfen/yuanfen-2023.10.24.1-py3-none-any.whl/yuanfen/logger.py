import logging
import os
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, logger_name):
        os.makedirs("logs", exist_ok=True)

        log_formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] [%(name)-16s] %(message)s")

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(log_formatter)

        self.file_handler = TimedRotatingFileHandler(
            "logs/log",
            when="midnight",
            backupCount=365,
            encoding="utf-8",
        )
        self.file_handler.suffix = "%Y-%m-%d.log"
        self.file_handler.setFormatter(log_formatter)

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level=logging.INFO)
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def debug(self, msg):
        self.logger.debug(f"{msg}")

    def info(self, msg):
        self.logger.info(f"{msg}")

    def warn(self, msg):
        self.logger.warning(f"{msg}")

    def error(self, msg):
        self.logger.error(f"{msg}")
