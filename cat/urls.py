
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
#from django.views.generic.list import BaseListView
from cat.models import MuseumObject, CulturalBloc, Person, Place


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

class HomeListView(ListView):
    model = MuseumObject
    paginate_by = 20
    def get_queryset(self):
        return MuseumObject.objects.exclude(artefactrepresentation__isnull=True).exclude(artefact_type__name='Tapacloth').exclude(artefact_type__name='Waistskirt')

urlpatterns = patterns('cat.views',
    url(r'^$', 
        HomeListView.as_view(template_name='../templates/index.html'), name='index'),
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

    url(r'^person/$',
        ListView.as_view(
            model=Person), name='person_list'),
    url(r'^person/(?P<pk>\d+)$',
        DetailView.as_view(
            model=Person), name="person_detail"),

    url(r'^country/$', 'all_countries', name='country_list'),
    url(r'^country/(.+)/$', 'regions', name='country_region_list'),
    
    url(r'^region/$', 'all_regions', name='all_regions_list'),
    url(r'^region/(.+)/$',
        RegionListView.as_view(), name='region_list'),

    url(r'^place/$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^place/(?P<place_id>\d+)$', 'place_detail', name='place_detail'),

    url(r'^withimages/$', 
        WithImagesListView.as_view(template_name='cat/withimages.html'), name='with_images_list'),

)
