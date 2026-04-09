from rest_framework.throttling import SimpleRateThrottle

class PathRateThrottle(SimpleRateThrottle):

    """
    Rate limit per user (or IP) per URL path.
    Example: /api/courses/ and /api/courses/1/ are counted separately.
    """
    scope = "path"
    
    def get_cache_key(self, request, view):
        # Identify caller: user id if authenticated, else IP
        if request.user and request.user.is_authenticated:
            ident = f"user:{request.user.pk}"
        else:
            ident = f"ip:{self.get_ident(request)}"

        path = request.path.rstrip("/")  # normalize trailing slash
        return f"throttle:{ident}:{path}"