import time
import logging

logger = logging.getLogger(__name__)


class LatencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        latency = end_time - start_time
        if hasattr(request, "user") and request.user.is_authenticated:
            # Log the latency for authenticated users
            logger.info(
                f"Latency for {request.method} {request.path} ({request.user.username}): {latency:.3f}s"
            )
        else:
            # Log the latency for anonymous users
            logger.info(f"Latency for {request.method} {request.path}: {latency:.3f}s")
        return response
