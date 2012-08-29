from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.syndication.views import add_domain
import urllib


def get_site_url(site, path):
    """Retrieve current site site

    Always returns as http (never https)
    """
    return add_domain(site.domain, path, False)


def do_paging(request, queryset):
    paginator = Paginator(queryset, 16)

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


def split_list(alist, parts=1):
    """
    Split a list into a number of parts
    http://stackoverflow.com/a/752562/119603
    """
    length = len(alist)
    return [ alist[i*length // parts: (i+1)*length // parts] 
             for i in range(parts) ]