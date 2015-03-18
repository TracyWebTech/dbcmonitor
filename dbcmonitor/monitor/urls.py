from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    url(r'^$', 'monitor.views.home', name='home'),

    url(r'^checkreplication/?', 'monitor.views.check_replication',
        name='check_replications'),
)
