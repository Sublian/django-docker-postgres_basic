from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        # limitamos por IP
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}
