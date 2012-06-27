from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.syndication.views import add_domain
from django.contrib.sites.models import get_current_site
import urllib


def get_site_url(request, path):
    """Retrieve current site site

    Always returns as http (never https)
    """
    current_site = get_current_site(request)
    site_url = add_domain(current_site.domain, path, request.is_secure())
    return site_url.replace('https', 'http')



def do_paging(request, queryset):
    paginator = Paginator(queryset, 25)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    return objects


def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs, True)
