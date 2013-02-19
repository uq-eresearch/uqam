from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from common.views import HomepageView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url('', include('uqam.cat.urls')),

    url(r'^$', HomepageView.as_view()),

    url(r'^about/$', TemplateView.as_view(template_name="about.html")),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dashboard/', include('uqam.dashboard.urls')),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^collection/', include('subcollections.urls')),

    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='auth_login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/', 'redirect_field_name': 'next'},
        name='auth_logout'),

    url(r'^', include('common.urls')),

    url(r'^place/', include('location.urls')),

    url(r'^mediaman/', include('mediaman.urls')),

    url(r'^people/', include('parties.urls')),

    url(r'^chaining/', include('smart_selects.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
