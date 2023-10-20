from datetime import datetime
import time
import traceback

from django.contrib import admin
from django.db import connection
from django.shortcuts import redirect
from django.template.defaultfilters import linebreaksbr
from django.urls import include, path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince


from ..models import ExceptionModel, Sql


class SqlAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "execute_btn",
        "success",
        "executed_at",
        "executed_at_time",
        "executed_at_timesince",
    ]
    list_filter = [
        "name",
        "success",
    ]
    list_search = [
        "name",
        "sql",
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "django_sql_executor/<int:pk>",
                self.admin_site.admin_view(self.execute_sql),
                name="django_sql_executor",
            )
        ]
        return custom_urls + urls

    def executed_at_time(self, obj):
        if obj.executed_at:
            return datetime.fromtimestamp(obj.executed_at)

    def executed_at_timesince(self, obj):
        if obj.executed_at:
            dt = datetime.fromtimestamp(obj.executed_at)
            return timesince(dt).split(",")[0] + " ago"

    executed_at_timesince.short_description = ""

    def execute_btn(self, obj):
        return format_html(
            '<a class="button" href="{}">EXECUTE</a> ',
            reverse("admin:django_sql_executor", args=[obj.pk]),
        )

    execute_btn.short_description = ""
    execute_btn.allow_tags = True

    def execute_sql(self, request, pk):
        cursor = connection.cursor()
        obj = Sql.objects.get(pk=pk)
        try:
            cursor.execute(obj.sql)
            Sql.objects.filter(pk=pk).update(
                success=True, executed_at=round(time.time(), 3)
            )
            url = reverse(
                "admin:{}_{}_changelist".format(
                    Sql._meta.app_label, Sql._meta.model_name
                )
            )
        except Exception as e:
            Sql.objects.filter(pk=pk).update(
                success=False, executed_at=round(time.time(), 3)
            )
            exc = ExceptionModel.objects.create(
                sql=obj.sql,
                exc_class="%s.%s" % (type(e).__module__, type(e).__name__),
                exc_value=str(e),
                exc_traceback=traceback.format_exc(),
                timestamp=round(time.time(), 3),
            )
            url = reverse(
                "admin:{}_{}_change".format(
                    ExceptionModel._meta.app_label, ExceptionModel._meta.model_name
                ),
                args=(exc.pk,),
            )
        return redirect(url)


admin.site.register(Sql, SqlAdmin)
