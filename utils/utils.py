from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.syndication.views import add_domain
from django.contrib.sites.models import get_current_site


def get_site_url(request, path):

    current_site = get_current_site(request)
    return add_domain(current_site.domain, path, request.is_secure())

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
