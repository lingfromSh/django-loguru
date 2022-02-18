# Standard Library
import time
from logging import getLogger

# Third Party Library
from django.utils.deprecation import MiddlewareMixin

middleware_logger = getLogger("dj_loguru.middleware.request_log")


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.entered_at = time.time()

    def process_response(self, request, response):
        response = response or self.get_response(request)
        message = "[STATUS {status_code} | COST {cost}ms] {method} {url}".format(
            status_code=response.status_code,
            cost=round((time.time() - request.entered_at) * 1000, 3),
            method=request.method,
            url=request.get_full_path(),
        )
        middleware_logger.info(message)
        return response
