
from django.conf.urls.defaults import patterns, url



urlpatterns = patterns('uqamcollections.views',
    url(r'^$', 'collections_home', name='collections_home'),

    url(r'^(\d+)$', 'collection_detail', name='collection_detail'),

    url(r'^add_objects', 'collection_add', name='collection_add'),

)
