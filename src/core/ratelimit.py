import time
from functools import wraps

from django.core.cache import cache
from django.http import JsonResponse


def client_key(request):
    if request.user.is_authenticated:
        return f'u{request.user.pk}'
    if request.session.session_key:
        return f's{request.session.session_key}'
    return f'ip{request.META.get("REMOTE_ADDR", "")}'


def ratelimit(scope, limit, window=60):
    """Fixed-window limiter backed by the cache: `limit` calls per `window` seconds."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            bucket = int(time.time() // window)
            key = f'rl:{scope}:{client_key(request)}:{bucket}'
            if cache.add(key, 1, window):
                count = 1
            else:
                try:
                    count = cache.incr(key)
                except ValueError:
                    count = 1
            if count > limit:
                return JsonResponse({'error': 'rate_limited'}, status=429)
            return view(request, *args, **kwargs)

        return wrapped

    return decorator
