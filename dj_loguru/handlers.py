import logging
from loguru import logger as loguru_logger


class DjangoLoguruHandler(logging.Handler):
    def __init__(self, level=0, **kwargs):
        self.kwargs = kwargs
        super(DjangoLoguruHandler, self).__init__(level)

    def emit(self, record) -> None:
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelname

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.bind(logger_name=record.name).opt(
            exception=record.exc_info, depth=depth, colors=True, lazy=True
        ).log(level, record.getMessage())
