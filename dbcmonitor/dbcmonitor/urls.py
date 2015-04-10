from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',

    url(r'^$', RedirectView.as_view(url='/monitor')),

    url(r'^monitor/', include('monitor.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
