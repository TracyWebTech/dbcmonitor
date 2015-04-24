
from django.contrib import admin
from .models import Database, Replication, ReplicationStatus, ReplicationError


class DatabaseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Replication)
admin.site.register(ReplicationStatus)
admin.site.register(ReplicationError)
