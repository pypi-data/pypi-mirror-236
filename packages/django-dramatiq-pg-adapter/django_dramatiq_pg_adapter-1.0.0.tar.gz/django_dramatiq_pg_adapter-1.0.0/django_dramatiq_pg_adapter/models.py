from django.conf import settings
from django.db import models
from django.utils import timezone
from django_dramatiq_pg_adapter.utils import get_tablename

PREFIX = getattr(settings, "DRAMATIQ_PG_PREFIX", "dramatiq_")


class PgDramatiqTask(models.Model):
    class STATE(models.TextChoices):
        QUEUED = "queued"
        CONSUMED = "consumed"
        REJECTED = "rejected"
        DONE = "done"

    message_id = models.UUIDField(primary_key=True)
    queue_name = models.TextField(default="default")
    state = models.CharField(max_length=16, default=STATE.QUEUED, choices=STATE.choices)
    mtime = models.DateTimeField(default=timezone.now)
    message = models.JSONField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    result_ttl = models.DateTimeField()

    class Meta:
        managed = False
        db_table = get_tablename(PREFIX)
        indexes = (models.Index(fields=["state", "mtime"]),)
