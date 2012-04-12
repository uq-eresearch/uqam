from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^search_home$', 'search_home2', name='search'),
)
