from django.conf.urls.defaults import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from views import PersistentSearchView

sqs = SearchQuerySet().facet('categories').facet('country').facet('has_images').facet('global_region').facet('item_name')


urlpatterns = patterns('common.views', #'haystack.views',
    # url(r'^search/$', search_view_factory(
    #         view_class=PersistentSearchView,
    #         form_class=FacetedSearchForm,
    #         searchqueryset=sqs
    #     ), name='haystack_search'),
    url(r'^search/$', 'catalogue_search', name='haystack_search'),
)
