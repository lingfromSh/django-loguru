from django.apps import AppConfig

# Standard Library
import logging
import logging.config

# Third Party Library
from django.conf import settings

from .handlers import DjangoLoguruHandler
from .utils import configure_logging


class DjangoLoguruConfig(AppConfig):
    name = "dj_loguru"

    def ready(self) -> None:
        # annotate all basicConfig with @overload in pycharm logger lib,
        # if reporting unexpected parameters in pycharm
        logging.basicConfig(handlers=[DjangoLoguruHandler()], level=0, force=True)
        configure_logging(settings.LOGGING)
