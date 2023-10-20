__all__ = [
    "Migration",
]

from django.db import models


class Migration(models.Model):
    app = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        db_table = "django_migrations"
        managed = False
