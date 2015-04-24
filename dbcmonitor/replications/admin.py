
from django.contrib import admin
from .models import Replication, ReplicationStatus, ReplicationError


admin.site.register(Replication)
admin.site.register(ReplicationStatus)
admin.site.register(ReplicationError)
