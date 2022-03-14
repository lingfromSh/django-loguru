"""
RequestLogMiddleware.py
"""

# Standard Library
import time
from logging import getLogger

# Third Party Library
from django.utils.deprecation import MiddlewareMixin

middleware_logger = getLogger("dj_loguru.middleware.request_log")


class RequestLogMiddleware(MiddlewareMixin):
    """
    A middleware for logging info of requests.
    """

    def process_request(self, request):
        """
        Inject entered_at into request
        """
        request.entered_at = time.time()

    def process_response(self, request, response):
        """
        Log response.
        """
        response = response or self.get_response(request)
        status_code=response.status_code
        cost=round((time.time() - request.entered_at) * 1000, 3)
        method = request.method
        url=request.get_full_path()
        message = f"[STATUS {status_code} | COST {cost}ms] {method} {url}"
        middleware_logger.info(message)
        return response
