from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',  # noqa
    url(r'^$', 'core.views.dashboard'),

    url(r'^monitor/', include('replications.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
