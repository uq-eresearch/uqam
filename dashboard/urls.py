
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import RedirectView




urlpatterns = patterns('dashboard.views',

#    url(r'^$',
#            RedirectView.as_view(url='/collector/a/'), name='collector_list'),
#    url(r'^collector/(?P<letter>[a-z])/$',
#        PeopleListView.as_view(
#            model=Person,
#            counted_obj='collected_objects',
#            view_name='collector_list',
#            page_title='Collectors',
#        ), name='collector_list'),
)
