from django.conf.urls.defaults import patterns, include, url

from haystack.views import search_view_factory
from views import PersistentSearchView


urlpatterns = patterns('haystack.views',
    #(r'^search/', include('haystack.urls')),
    url(r'^search/', search_view_factory(
        view_class=PersistentSearchView
        ), name='haystack_search'),
)
