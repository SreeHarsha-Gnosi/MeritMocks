import mimetypes

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Windows registries often map these to text/plain; with nosniff the
        # browser would then refuse to apply our CSS or run our JS.
        mimetypes.add_type('text/css', '.css', strict=True)
        mimetypes.add_type('text/javascript', '.js', strict=True)
        mimetypes.add_type('image/svg+xml', '.svg', strict=True)
