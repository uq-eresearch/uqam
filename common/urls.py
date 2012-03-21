from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^search_home$', 'search_home', name='search'),
    url(r'^search_results$', 'search_home',
        {'template_name': 'common/search_results.html'},
        name='search_results'),
    url(r'^search_xls$', 'search_xls', name='search_xls'),
)
