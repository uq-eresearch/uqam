import copy
from django.conf import settings
from django import template

register = template.Library()


@register.inclusion_tag('django_xsession/loader.html', takes_context=True)
def xsession_loader(context):

    try:
        request = context['request']
    except KeyError:
        return {}

    # Check if XSessionMiddleware was loaded
    if not hasattr(request, 'xsession'):
        return {}

    # Try to load session
    # cookie = settings.__dict__.get('SESSION_COOKIE_NAME', 'sessionid')
    # try:
    #     sessionid = request.COOKIES[cookie]
    # except KeyError, AttributeError:
    #     pass
    # else:
    #     return {}

    # Bad Idea, infinite reloading
    # But, maybe fixed with extra check in the middleware js generation 
    if request.user.is_authenticated():
        return {}

    # No session found
    try:
        host = request.META['HTTP_HOST']
    except KeyError:
        return {}

    # Build domain list
    # domains = copy.copy(settings.XSESSION_DOMAINS)
    domains = [domain for domain in settings.XSESSION_DOMAINS if host not in domain]

    render_context = {
        'path': settings.__dict__.get('XSESSION_FILENAME', 'xsession_loader.js'),
        'domains': domains,
    }

    return render_context
