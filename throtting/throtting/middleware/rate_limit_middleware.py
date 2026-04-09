import time
import re
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser


class RateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        # ✅ GLOBAL default for ALL /api/*
        self.LIMIT = 10
        self.WINDOW = 60  # seconds

    def __call__(self, request):
        path = request.path

        # Ignore static and favicon
        if path.startswith("/static/") or path == "/favicon.ico":
            return self.get_response(request)

        # Apply only to /api/
        if not path.startswith("/api/"):
            return self.get_response(request)

        # Identify user or IP
        user = getattr(request, "user", AnonymousUser())
        if user and getattr(user, "is_authenticated", False):
            ident = f"user:{user.pk}"
        else:
            ident = f"ip:{self.get_ip(request)}"

        # Normalize path (so /1 /2 /3 use same bucket)
        normalized_path = self.normalize_path(path)

        now = int(time.time())
        bucket = now // self.WINDOW
        key = f"rl:{ident}:{normalized_path}:{bucket}:{self.WINDOW}"

        # Atomic increment (Redis safe)
        try:
            current = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=self.WINDOW)
            current = 1

        # If limit exceeded
        if current > self.LIMIT:
            retry_after = self.WINDOW - (now % self.WINDOW)

            response = JsonResponse(
                {
                    "detail": "Too Many Requests",
                    "limit": self.LIMIT,
                    "window_seconds": self.WINDOW,
                    "retry_after_seconds": retry_after,
                    "path": normalized_path,
                },
                status=429,
            )

            response["Retry-After"] = str(retry_after)
            return response

        return self.get_response(request)

    def normalize_path(self, path: str) -> str:
        # /api/courses/12/ -> /api/courses/{id}/
        path = re.sub(r"/\d+(/|$)", "/{id}/", path + "/")
        return path.rstrip("/")

    def get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
