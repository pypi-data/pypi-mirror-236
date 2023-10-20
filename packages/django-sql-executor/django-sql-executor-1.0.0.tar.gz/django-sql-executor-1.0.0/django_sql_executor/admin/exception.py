from datetime import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from django.utils.timesince import timesince

from django.template.defaultfilters import linebreaksbr

from ..models import ExceptionModel


class ExceptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "exc_class",
        "exc_value",
        "sql_html",
        "time",
        "timesince",
    ]
    list_filter = [
        "exc_class",
    ]
    list_search = ["sql", "exc_class", "exc_value", "exc_traceback"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def sql_html(self, obj):
        return linebreaksbr(obj.sql.strip()) if obj.sql.strip() else None

    sql_html.short_description = "sql"
    sql_html.allow_tags = True

    def exc_traceback_html(self, obj):
        return linebreaksbr(obj.exc_traceback) if obj.exc_traceback else None

    exc_traceback_html.short_description = "traceback"
    exc_traceback_html.allow_tags = True

    def time(self, obj):
        return datetime.fromtimestamp(obj.timestamp)

    def timesince(self, obj):
        return "%s ago" % timesince(datetime.fromtimestamp(obj.timestamp))


admin.site.register(ExceptionModel, ExceptionAdmin)
