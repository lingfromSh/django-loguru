from django.apps import AppConfig

# Third Party Library
from django.conf import settings

from .utils import configure_logging


class DjangoLoguruConfig(AppConfig):
    name = "dj_loguru"

    def ready(self) -> None:
        configure_logging(settings.LOGGING)
