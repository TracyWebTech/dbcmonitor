from django.contrib import admin

from .models import Database

class DatabaseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Database, DatabaseAdmin)
