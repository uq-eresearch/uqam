
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import RedirectView
#from django.views.generic.list import BaseListView
from cat.models import MuseumObject, CulturalBloc
from parties.models import Person, Maker
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
        return MuseumObject.objects.exclude(
                artefactrepresentation__isnull=True)


urlpatterns = patterns('cat.views',
    url(r'^$', 'home_page', name='index'),
    url(r'^artefact/$',
        ListView.as_view(
            model=MuseumObject, paginate_by=20), name='artefact_list'),
    url(r'^artefact/(?P<slug>\d+)$',
        DetailView.as_view(slug_field='registration_number',
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

    url(r'^withimages/$',
        WithImagesListView.as_view(
            template_name='cat/withimages.html'), name='with_images_list'),

    url(r'^categories/$', 'categories_list', name='categories_list'),

    url(r'^categories/(?P<full_slug>.+)/$', 'categories_list',
        name='categories_list'),

    url(r'^person/$',
        TemplateView.as_view(template_name="parties/person.html"),
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
# Custom search to redirect straight to objects
#    url(r'^search/', 'search', name='search'),
)
