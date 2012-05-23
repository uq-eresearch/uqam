from django.http import HttpResponsePermanentRedirect
from django.conf import settings

# From : http://www.redrobotstudios.com/blog/2010/02/06/requiring-https-for-certain-paths-in-django/


class SecureRequiredMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')

    def process_request(self, request):
        if self.enabled and not request.is_secure():
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None
#In settings.py
#
#MIDDLEWARE_CLASSES = (
#...
#    'myproject.middleware.SecureRequiredMiddleware',
#)
#
#HTTPS_SUPPORT = True
#SECURE_REQUIRED_PATHS = (
#    '/admin/',
#    '/accounts/',
#    '/management/',
#)

