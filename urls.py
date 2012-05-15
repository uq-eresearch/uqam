from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('', include('uqam.cat.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dashboard/', include('uqam.dashboard.urls')),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^collection/', include('uqamcollections.urls')),

    (r'^search/', include('haystack.urls')),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='auth_login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/', 'redirect_field_name': 'next'},
        name='auth_logout'),

    url(r'^report/', include('reports.urls')),
    url(r'^', include('common.urls')),

    url(r'^place/', include('location.urls')),

    url(r'^mediaman/', include('mediaman.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
