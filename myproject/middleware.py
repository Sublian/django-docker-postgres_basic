import logging
import time

logger = logging.getLogger("django.request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = round(time.time() - start_time, 3)

        user = request.user if request.user.is_authenticated else "Anonymous"
        ip = request.META.get("REMOTE_ADDR")
        path = request.path
        method = request.method
        status = response.status_code

        logger.warning(
            f"{method} {path} | status={status} | user={user} | ip={ip} | {duration}s"
        )

        return response
