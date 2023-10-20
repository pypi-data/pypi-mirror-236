from django.contrib import admin
from django.utils.timesince import timesince

from .models import Migration


class MigrationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "app",
        "name",
        "applied",
        "timesince",
    ]
    search_fields = ["name"]
    list_filter = [
        "app",
    ]

    def timesince(self, obj):
        return timesince(obj.applied) + " ago"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Migration, MigrationAdmin)
