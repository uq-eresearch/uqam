
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from cat.models import MuseumObject, CulturalBloc, Person, Place


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

    url(r'^place/$',
        ListView.as_view(
            model=Place), name='place_list'),
    url(r'^place/(?P<pk>\d+)$',
        DetailView.as_view(
            model=Place), name="place_detail"),

    url(r'^table/$', 'table', name='table'),
)
