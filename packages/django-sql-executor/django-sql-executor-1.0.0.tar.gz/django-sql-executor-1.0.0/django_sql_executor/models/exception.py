__all__ = [
    "ExceptionModel",
]


from django.db import models


class ExceptionModel(models.Model):
    sql = models.TextField(null=True, editable=False)
    exc_class = models.TextField(editable=False, verbose_name="class")
    exc_value = models.TextField(editable=False, verbose_name="value")
    exc_traceback = models.TextField(editable=False, verbose_name="traceback")
    timestamp = models.FloatField(editable=False)

    class Meta:
        db_table = "sql_executor_exception"
        ordering = ("-timestamp",)
        verbose_name = "Exception"
        verbose_name_plural = "Exceptions"
