from django.contrib import admin
from monitor.models import Organization, Replication, SlaveReplication, \
    DatabaseStatus, TableStatus

admin.site.register(Organization)
admin.site.register(Replication)
admin.site.register(SlaveReplication)
admin.site.register(DatabaseStatus)
admin.site.register(TableStatus)
