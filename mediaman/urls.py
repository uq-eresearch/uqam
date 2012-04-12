from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('mediaman.views',
    url(r'bulk_upload', 'bulk_upload', name='bulk_upload'),
)
