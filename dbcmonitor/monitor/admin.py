from django.contrib import admin
from monitor.models import Replication, SlaveReplication, DatabaseStatus, \
    TableStatus

admin.site.register(Replication)
admin.site.register(SlaveReplication)
admin.site.register(DatabaseStatus)
admin.site.register(TableStatus)
