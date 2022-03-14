from logging import getLogger
from django.test import TestCase

logger = getLogger("dj_loguru")


class DjLoguruTest(TestCase):
    def test_debug(self):
        logger.debug("Test debug.")

    def test_info(self):
        logger.info("Test info.")

    def test_error(self):
        logger.error("Test error.")

    def test_fatal(self):
        logger.fatal("Test fatal.")

    def test_critical(self):
        logger.critical("Test critical.")

    def test_exception(self):
        try:
            raise ValueError
        except ValueError:
            logger.exception("Exception hanppened.")