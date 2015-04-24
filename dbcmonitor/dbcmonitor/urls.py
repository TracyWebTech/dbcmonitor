from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',  # noqa
    url(r'^monitor/', include('replications.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^db/(?P<db_slug>[\w-]+)/$', 'core.views.dashboard'),

)
