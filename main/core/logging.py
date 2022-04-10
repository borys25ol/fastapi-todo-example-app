"""
Module configuration custom logger.
"""
import logging
from typing import List, Optional

DEFAULT_LOGGER_NAME = "fastapi-todo"

LOG_MESSAGE_FORMAT = "[%(name)s] [%(asctime)s] %(message)s"


class ProjectLogger:
    """
    Custom project logger.
    """

    def __init__(self, name: str):
        self.name = name
        self._logger: Optional[logging.Logger] = None

    def __call__(self, *args: tuple, **kwargs: dict) -> logging.Logger:
        return self.logger

    @property
    def logger(self) -> logging.Logger:
        """
        Return initialized logger object.
        """
        if not self._logger:
            self._logger = self.create_logger()
        return self._logger

    def create_logger(self) -> logging.Logger:
        """
        Return configured logger.
        """
        logging.basicConfig(format=LOG_MESSAGE_FORMAT)

        custom_logger = logging.getLogger(name=self.name)
        custom_logger.setLevel(level=logging.INFO)

        return custom_logger


def create_logger(name: str = DEFAULT_LOGGER_NAME) -> logging.Logger:
    """
    Initialize logger for project.
    """
    return ProjectLogger(name=name)()


logger = create_logger()
