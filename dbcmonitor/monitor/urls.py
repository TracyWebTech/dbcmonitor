from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',

    url(r'^$', 'monitor.views.dashboard', name='dashboard'),

    url(r'^checkreplication/?', 'monitor.views.check_replication',
        name='check_replications'),
    url(r'^send-status/?', 'monitor.views.save_replication_status',
        name='save_status'),
)
