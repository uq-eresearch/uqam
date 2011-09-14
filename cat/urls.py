
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
#from django.views.generic.list import BaseListView
from cat.models import MuseumObject, CulturalBloc, Person, Place


class CountryListView(ListView):
    model = MuseumObject
    paginate_by = 20

    def get_queryset(self):
        return MuseumObject.objects.filter(place__country=self.args[0])

class RegionListView(ListView):
    model = MuseumObject
    paginate_by = 20

    def get_queryset(self):
        return MuseumObject.objects.filter(place__region=self.args[0])

urlpatterns = patterns('cat.views',
    url(r'^$',
        TemplateView.as_view(
            template_name='index.html'), name='index'),
    url(r'^artefact/$',
        ListView.as_view(
            model=MuseumObject, paginate_by=20), name='artefact_list'),
    url(r'^artefact/(?P<pk>\d+)$',
        DetailView.as_view(
            model=MuseumObject), name='artefact_view'),

    url(r'^blocs/$',
        ListView.as_view(
            model=CulturalBloc), name='bloc_list'),
    url(r'^blocs/(?P<slug>.*)$',
        DetailView.as_view(
            model=CulturalBloc,
            slug_field='name'), name="culturalbloc_detail"),

    url(r'^person/$',
        ListView.as_view(
            model=Person), name='person_list'),
    url(r'^person/(?P<pk>\d+)$',
        DetailView.as_view(
            model=Person), name="person_detail"),

    
    url(r'^region/$', 'all_regions', name='all_regions_list'),
    url(r'^region/(.+)/$',
        RegionListView.as_view(), name='region_list'),

    url(r'^country/$', 'all_countries', name='country_list'),
    url(r'^country/(.+)/$',
        CountryListView.as_view(), name='country_list'),

    url(r'^place/$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^place/(?P<pk>\d+)$',
        DetailView.as_view(
            model=Place), name="place_detail"),

    url(r'^table/$', 'table', name='table'),
)
