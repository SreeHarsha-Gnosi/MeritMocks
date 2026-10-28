PERMISSIONS_POLICY = ', '.join([
    'camera=()',
    'microphone=()',
    'geolocation=()',
    'payment=()',
    'usb=()',
    'display-capture=()',
    'fullscreen=(self)',
])


class SecurityHeadersMiddleware:
    """Headers Django has no setting for, plus no-store on exam traffic.

    Exam pages and APIs must never be cached by the browser or a proxy:
    otherwise questions survive in the back/forward cache or disk cache after
    the test is over.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Permissions-Policy', PERMISSIONS_POLICY)
        response.setdefault('Cross-Origin-Resource-Policy', 'same-origin')
        if getattr(request, 'no_store', False) or request.path.startswith('/attempt/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
