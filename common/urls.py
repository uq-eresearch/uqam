from django.conf.urls.defaults import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from views import PersistentSearchView

sqs = SearchQuerySet().facet('categories').facet('people').facet('country').facet('has_images').facet('global_region')


urlpatterns = patterns('haystack.views',
    url(r'^search/$', PersistentSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
)
