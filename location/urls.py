from django.conf.urls.defaults import *

from django.views.generic import ListView
from location.models import Place

urlpatterns = patterns('location.views',

    url(r'^places$', 'view_places', name='view_places'),
    url(r'^tree_view$', 'tree_view', name='tree_view'),


    url(r'^(?P<loctype>[\w ]+)-(?P<id>\d+)$', 'view_geoloc', name='view_geoloc'),
#    url(r'^(?P<global_region>[\w_].)/$', 'view_geoloc', name='view_geoloc'),
#    url(r'^(?P<global_region>[\w_].)/(?P<country>[\w_].)/$', 'view_geoloc', name='view_geoloc'),

    url(r'^$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^kml$', 'place_kml', name='place_kml'),
    url(r'^json$', 'place_json', name='place_json'),
    url(r'^(?P<place_id>\d+)$', 'place_detail', name='place_detail'),

    url(r'^dups$', 'place_duplicates', name='place_duplicates'),
    url(r'^gn/(\d+)$', 'place_geoname'),

)
