from django.conf.urls.defaults import patterns, url
from feeds import AllCollectionsFeed, CollectionFeed



urlpatterns = patterns('uqamcollections.views',
    url(r'^$', 'collections_home', name='collections_home'),

    url(r'^(\d+)$', 'collection_detail', name='collection_detail'),

    url(r'^add_objects', 'collection_add', name='collection_add'),

    url(r'^feed/$', AllCollectionsFeed()),
    url(r'^(?P<collection_id>\d+)/xml$', CollectionFeed()),
    url(r'^(?P<collection_id>\d+)/atom$', 'atom_detail', name='collection_atom_detail'),


#    url(r'^(\d+)\xml$', 'collection_feed', name='collection_feed'),

)
