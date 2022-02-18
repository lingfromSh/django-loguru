import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from functools import partial
from loguru import logger as loguru_logger

BASE_LOGURU_LOGGING = {
    "formats": {
        "default": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> |"
        " <level>{level:<8}</level> |"
        " <cyan>{file}</cyan>:<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
        " - <level>{message}</level>"
    }
}


def gen_add_loguru_logger():
    __handlers__ = {}

    def add(identity, **kwargs):
        __handlers__[identity] = kwargs
        loguru_logger.configure(handlers=list(__handlers__.values()))

    return add


add_loguru_logger = gen_add_loguru_logger()


def get_logger_level(name):
    level = settings.LOGGING["levels"][name]
    return level.get("no") or level.get("priority")


def filter_by_logger_name(record, logger_name):
    return record["extra"]["logger_name"] == logger_name


def configure_logging(config):
    base_config = BASE_LOGURU_LOGGING
    base_config.update(config)
    config = base_config

    formats = config.get("formats", {})

    for level, setting in config.get("levels", {}).items():
        try:
            loguru_logger.level(level.upper())
        except ValueError:
            setting["no"] = setting.pop("priority", 0)
            loguru_logger.level(level.upper(), **setting)
            logging.addLevelName(setting["no"], level.upper())

    for logger_name, logger_setting in config.get("loggers", {}).items():
        if not logger_setting.get("sinks", []):
            continue

        sinks = config.get("sinks", {})
        for sink_name in logger_setting.get("sinks", []):
            if sink_name not in sinks:
                raise ImproperlyConfigured(
                    f"Sink {sink_name} cannot be configured successfully."
                )
            sink_setting = sinks[sink_name].copy()
            sink_setting["sink"] = sink_setting.pop("output", None)
            sink_setting["format"] = formats.get(
                sink_setting.get("format", "default"), None
            )
            sink_setting["filter"] = partial(
                filter_by_logger_name, logger_name=logger_name
            )
            sink_setting["level"] = logger_setting.get(
                "level", sink_setting.get("level", "DEBUG")
            )
            add_loguru_logger(identity=f"{logger_name}:{sink_name}", **sink_setting)
