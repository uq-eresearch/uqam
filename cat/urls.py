from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from cat.models import MuseumObject


urlpatterns = patterns('cat.views',

    url(r'^item/$',
        ListView.as_view(
            model=MuseumObject, paginate_by=20), name='artefact_list'),
    url(r'^item/(?P<reg_num>\d+)$', 'item_detail', name='artefact_view'),



    url(r'^categories/$', 'categories_browse', name='categories_list'),

    url(r'^categories/(?P<full_slug>.+)/$', 'categories_list',
        name='categories_list'),

)
