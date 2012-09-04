from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('common.views',
    url(r'^search/$', 'catalogue_search', name='haystack_search'),
)
