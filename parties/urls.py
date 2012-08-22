from django.conf.urls.defaults import *
from models import Person, Maker
from django.views.generic import DetailView, ListView

# place app url patterns here

urlpatterns = patterns('parties.views',
    url('browse/', 'people_aggregate', name='parties_browse'),
)
