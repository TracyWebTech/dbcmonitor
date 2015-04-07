from django.contrib import admin
from monitor.models import Organization, Replication, ReplicationStatus, \
    Database, Table, TableStatus

admin.site.register(Organization)
admin.site.register(Replication)
admin.site.register(ReplicationStatus)
admin.site.register(Database)
admin.site.register(Table)
admin.site.register(TableStatus)
