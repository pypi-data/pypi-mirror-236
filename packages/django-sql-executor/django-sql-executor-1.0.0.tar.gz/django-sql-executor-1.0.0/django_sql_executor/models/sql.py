__all__ = [
    "Sql",
]


from django.db import models


class Sql(models.Model):
    name = models.CharField(unique=True, max_length=255)
    sql = models.TextField()
    success = models.BooleanField(null=True, editable=False)

    executed_at = models.FloatField(null=True, editable=False, verbose_name="executed")

    class Meta:
        db_table = "sql_executor_sql"
        ordering = ("-executed_at",)
