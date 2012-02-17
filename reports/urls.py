from django.conf.urls.defaults import *

urlpatterns = patterns('reports.views',
    url(r'^view/(\d+)$', 'view_report', name='view_report'),
)
