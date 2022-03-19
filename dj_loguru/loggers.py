from functools import partial
from logging import Logger
from django.conf import settings


class DjangoLoguruLogger(Logger):
    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """
        if isinstance(level, str):
            level = (
                settings.LOGGING.get("levels", {}).get(level, {}).get("no")
            )
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            level = (
                settings.LOGGING.get("levels", {})
                .get(name.upper(), {})
                .get("no")
            )
            if not level:
                raise AttributeError(
                    f"DjangoLoguruLogger has not attribute {name}"
                )
            func = partial(self.log, level)
            return func
