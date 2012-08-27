
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import RedirectView
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
#    url(r'^$', 'home_page', name='index'),

    url(r'^item/$',
        ListView.as_view(
            model=MuseumObject, paginate_by=20), name='artefact_list'),
    url(r'^item/(?P<reg_num>\d+)$', 'item_detail', name='artefact_view'),
#        DetailView.as_view(slug_field='registration_number',
 #           model=MuseumObject), name='artefact_view'),



    url(r'^withimages/$',
        WithImagesListView.as_view(
            template_name='cat/withimages.html'), name='with_images_list'),

    url(r'^categories/$', 'categories_list', name='categories_list'),

    url(r'^categories/(?P<full_slug>.+)/$', 'categories_list',
        name='categories_list'),

# Custom search to redirect straight to objects
#    url(r'^search/', 'search', name='search'),
)
