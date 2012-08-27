from django.conf.urls.defaults import *

# place app url patterns here

urlpatterns = patterns('parties.views',
    url('browse/', 'people_aggregate', name='parties_browse'),

    url(r'^person/(?P<pk>\d+)$', 'person_detail', name="person_detail"),
    url(r'^person/(?P<pk>\d+)/(?P<item_type>\w+)$', 'person_detail', name="person_detail"),
)
