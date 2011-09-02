
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView
from cat.models import MuseumObject, CulturalBloc, Person


urlpatterns = patterns('cat.views',
    url(r'^$', 'index', name='index'),
    url(r'^artefact/(?P<pk>\d+)$',
        DetailView.as_view(
            model=MuseumObject), name='artefact_view'),
    url(r'^blocs/(?P<slug>.*)$',
        DetailView.as_view(
            model=CulturalBloc,
            slug_field='name'), name="culturalbloc_detail"),
    url(r'^person/(?P<pk>\d+)$',
        DetailView.as_view(
            model=Person), name="person_detail"),
    url(r'^table/$', 'table', name='table'),
)
