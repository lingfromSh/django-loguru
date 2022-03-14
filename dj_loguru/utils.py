import logging
import sys
from copy import deepcopy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from functools import partial
from loguru import logger as loguru_logger

BASE_LOGURU_LOGGING = {
    "formats": {"default": "<level>{message}</level>"},
    "sinks": {
        "console": {
            "output": sys.stderr,
            "format": "default",
            "level": "DEBUG",
        }
    },
    "loggers": {"root": {"sinks": ["console"], "level": "DEBUG"}},
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


def filter_by_logger_name(record, logger_name, propagate=False):
    splited_extra_logger_name = record["extra"]["logger_name"].split(".")
    splited_logger_name = logger_name.split(".")

    if propagate and len(splited_logger_name) <= len(splited_extra_logger_name):
        return all(
            (
                item == splited_extra_logger_name[idx]
                for idx, item in enumerate(splited_logger_name)
            )
        )
    else:
        return splited_logger_name == splited_extra_logger_name


def merge_dict(a: dict, b: dict):
    ret = {**a}

    for k, v in b.items():
        if k in ret and isinstance(ret[k], dict):
            merged = merge_dict(ret[k], v)
            ret.update({k: merged})
        else:
            ret.update({k: v})
    return ret


def configure_logging(config):
    config = merge_dict(BASE_LOGURU_LOGGING, config)
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

        propagate = logger_setting.get("propagate", True)
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
                filter_by_logger_name, logger_name=logger_name, propagate=propagate
            )
            sink_setting["level"] = logger_setting.get(
                "level", sink_setting.get("level", "DEBUG")
            )
            add_loguru_logger(identity=f"{logger_name}:{sink_name}", **sink_setting)
