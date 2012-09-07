from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('mediaman.views',
    url(r'bulk_upload', 'bulk_upload', name='bulk_upload'),
    url(r'handle_upload', 'handle_upload', name='handle_upload'),
    url(r'set_photographer', 'set_photographer', name='set_photographer'),
)
