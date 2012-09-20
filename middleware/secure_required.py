from django.http import HttpResponseRedirect
from django.conf import settings

# From : http://www.redrobotstudios.com/blog/2010/02/06/requiring-https-for-certain-paths-in-django/


class SecureRequiredMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')
        self.public_domain = 'anth-real.uqdayers.local'
        self.secure_domain = 'anth.metadata.net.local'

    def process_request(self, request):
        # if self.enabled and not request.is_secure():
        if self.enabled:
            if request.get_full_path().startswith('/xsession_loader.js'):
                return None

            secure_path = False
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    secure_path = True

            if secure_path and not request.is_secure():
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace(self.public_domain, self.secure_domain)
                secure_url = secure_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
            if not secure_path and request.is_secure():
                request_url = request.build_absolute_uri(request.get_full_path())
                public_url = request_url.replace(self.secure_domain, self.public_domain)
                public_url = public_url.replace('https://', 'http://')
                return HttpResponseRedirect(public_url)
        return None

    def process_response(self, request, response):
        """
        Ensure we only redirect to correct secure/non-secure domain
        """
        if self.enabled and isinstance(response, HttpResponseRedirect):
            location = response['Location']
            for path in self.paths:
                if path in location and self.secure_domain in location:
                    response['Location'] = location.replace('http://', 'https://').replace(
                        self.public_domain, self.secure_domain)
                    return response

            if 'http' in location:
                if 'https' in location:
                    response['Location'] = location.replace('https://', 'http://').replace(
                        self.secure_domain, self.public_domain)
            else:
                response['location'] = 'http://' + self.public_domain + location
        return response
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

