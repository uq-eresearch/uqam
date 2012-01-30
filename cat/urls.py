
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import RedirectView
#from django.views.generic.list import BaseListView
from cat.models import MuseumObject, CulturalBloc, Person, Place, Maker
from cat.views import PeopleListView


class CountryListView(ListView):
    model = MuseumObject
    paginate_by = 20
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['name'] = self.args[0]
        return context
    def get_queryset(self):
        return MuseumObject.objects.filter(place__country=self.args[0])

class RegionListView(CountryListView):
    def get_queryset(self):
        return MuseumObject.objects.filter(place__region=self.args[0])

class CulturalBlocListView(CountryListView):
    def get_queryset(self):
        return MuseumObject.objects.filter(cultural_bloc__name=self.args[0])

class WithImagesListView(ListView):
    model = MuseumObject
    paginate_by = 20
    def get_queryset(self):
        return MuseumObject.objects.exclude(artefactrepresentation__isnull=True)


urlpatterns = patterns('cat.views',
    url(r'^$', 'home_page', name='index'),
    url(r'^artefact/$',
        ListView.as_view(
            model=MuseumObject, paginate_by=20), name='artefact_list'),
    url(r'^artefact/(?P<pk>\d+)$',
        DetailView.as_view(
            model=MuseumObject), name='artefact_view'),

    url(r'^blocs/$',
        ListView.as_view(
            model=CulturalBloc), name='bloc_list'),
    url(r'^blocs/(.*)$',
        CulturalBlocListView.as_view(), name='culturalbloc_detail'),


    url(r'^country/$', 'all_countries', name='country_list'),
    url(r'^country/(.+)/$', 'regions', name='country_region_list'),

    url(r'^region/$', 'all_regions', name='all_regions_list'),
    url(r'^region/(.+)/$',
        RegionListView.as_view(), name='region_list'),

    url(r'^place/$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^place/kml$', 'place_kml', name='place_kml'),
    url(r'^place/map$', 'place_map', name='place_map'),
    url(r'^place/map_cluster$', 'place_mapcluster', name='place_mapcluster'),
    url(r'^place/json$', 'place_json', name='place_json'),
    url(r'^place/(?P<place_id>\d+)$', 'place_detail', name='place_detail'),

    url(r'^place/dups$', 'place_duplicates', name='place_duplicates'),
    url(r'place/gn/(\d+)$', 'place_geoname'),

    url(r'^withimages/$',
        WithImagesListView.as_view(template_name='cat/withimages.html'), name='with_images_list'),

    url(r'^categories/$', 'categories_list', name='categories_list'),

    url(r'^categories/(?P<full_slug>.+)/$', 'categories_list', name='categories_list'),

    url(r'^person/$',
        TemplateView.as_view(template_name="cat/person.html"),
        name='person_list'),
    url(r'^person/(?P<pk>\d+)$',
        DetailView.as_view(model=Person), name="person_detail"),

    url(r'^maker/$',
            RedirectView.as_view(url='/maker/a/'), name='maker_list'),
    url(r'^maker/(?P<letter>[a-z])/$',
        PeopleListView.as_view(
            model=Maker,
            view_name='maker_list',
            page_title='Makers',
        ), name='maker_list'),
    url(r'^maker/(?P<pk>\d+)/$',
        DetailView.as_view(model=Maker), name='maker_detail'),


    url(r'^donor/$',
            RedirectView.as_view(url='/donor/a/'), name='donor_list'),
    url(r'^donor/(?P<letter>[a-z])/$',
        PeopleListView.as_view(
            model=Person,
            counted_obj='donated_objects',
            view_name='donor_list',
            page_title='Donors',
        ), name='donor_list'),

    url(r'^collector/$',
            RedirectView.as_view(url='/collector/a/'), name='collector_list'),
    url(r'^collector/(?P<letter>[a-z])/$',
        PeopleListView.as_view(
            model=Person,
            counted_obj='collected_objects',
            view_name='collector_list',
            page_title='Collectors',
        ), name='collector_list'),
    url(r'^search/', 'search', name='search'),
)
