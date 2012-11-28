from django.http import HttpResponseRedirect
from django.conf import settings

# From : http://www.redrobotstudios.com/blog/2010/02/06/requiring-https-for-certain-paths-in-django/


class SecureRequiredMiddleware(object):
    """
    Django Middleware to enforce viewing some urls only over HTTPS

    Has (crazy) support for using a different hostname to access HTTPS,
    which can be useful if there are limits on the SSL certificate.

    For these multiple hostname shenanigans to work, Xsession middleware
    is also required.
    """

    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')
        self.public_domain = getattr(settings, 'PUBLIC_DOMAIN')
        self.secure_domain = getattr(settings, 'SECURE_DOMAIN')

    def process_request(self, request):
        if self.enabled:
            if request.get_full_path().startswith('/xsession_loader.js'):
                return None

            secure_path = False
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    secure_path = True

            request_url = request.build_absolute_uri(request.get_full_path())

            new_url = request_url
            if secure_path and not request.is_secure():
                new_url = request_url.replace(self.public_domain, self.secure_domain)
                new_url = new_url.replace('http://', 'https://')

            if not secure_path and (request.is_secure() or self.secure_domain in request_url):
                new_url = request_url.replace(self.secure_domain, self.public_domain)
                new_url = new_url.replace('https://', 'http://')

            if new_url and new_url != request_url:
                return HttpResponseRedirect(new_url)
        return None

    def process_response(self, request, response):
        """
        Ensure we only redirect to correct secure/non-secure domain
        """
        if self.enabled and isinstance(response, HttpResponseRedirect):
            location = response['Location']
            if location.startswith('..'):
                return response
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

