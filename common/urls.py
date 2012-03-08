from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^search_home$', 'search_home', name='search'),
)
