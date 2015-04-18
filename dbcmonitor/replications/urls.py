from django.conf.urls import patterns, url

from .views import dashboard, check_replication, save_replication_status

urlpatterns = patterns(
    '',

    url(r'^$', dashboard, name='dashboard'),
    url(r'^checkreplication/?', check_replication, name='check_replications'),
    url(r'^send-status/?', save_replication_status, name='save_status'),
)
