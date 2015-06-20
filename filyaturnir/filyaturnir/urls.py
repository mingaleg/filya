from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'filyaturnir.views.home', name='home'),
    # url(r'^filyaturnir/', include('filyaturnir.foo.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'singin.html'
    }),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('collector.urls')),
)
