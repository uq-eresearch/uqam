from django.conf.urls.defaults import *

from django.views.generic import ListView
from location.models import Place

urlpatterns = patterns('location.views',

    url(r'^$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^kml$', 'place_kml', name='place_kml'),
    url(r'^map$', 'place_map', name='place_map'),
    url(r'^map_cluster$', 'place_mapcluster', name='place_mapcluster'),
    url(r'^json$', 'place_json', name='place_json'),
    url(r'^(?P<place_id>\d+)$', 'place_detail', name='place_detail'),

    url(r'^dups$', 'place_duplicates', name='place_duplicates'),
    url(r'^gn/(\d+)$', 'place_geoname'),

)
