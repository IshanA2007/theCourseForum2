"""Middleware to handle health check requests without ALLOWED_HOSTS validation."""

from django.http import HttpResponse


class HealthCheckMiddleware:
    """Bypass ALLOWED_HOSTS for health check endpoint."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Short-circuit "/health" before the request reaches Django's host
        # validation so uptime probes (which hit the pod IP rather than a
        # configured ALLOWED_HOSTS entry) always get a plain 200 "ok".
        if request.path == "/health":
            return HttpResponse("ok")
        return self.get_response(request)
