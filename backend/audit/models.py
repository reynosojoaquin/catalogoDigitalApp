import uuid

from django.conf import settings
from django.db import models


class ImmutableAuditEventQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValueError("Audit events are append-only")

    def delete(self):
        raise ValueError("Audit events are append-only")

    def bulk_update(self, objs, fields, batch_size=None):
        raise ValueError("Audit events are append-only")


class AuditEvent(models.Model):
    class Result(models.TextChoices):
        SUCCESS = "success", "Success"
        DENIED = "denied", "Denied"
        FAILURE = "failure", "Failure"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120, db_index=True)
    resource_type = models.CharField(max_length=100, blank=True, db_index=True)
    resource_id = models.CharField(max_length=100, blank=True, db_index=True)
    result = models.CharField(max_length=10, choices=Result.choices, db_index=True)
    source = models.CharField(max_length=20, default="web")
    correlation_id = models.UUIDField(db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    objects = ImmutableAuditEventQuerySet.as_manager()

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["resource_type", "resource_id", "occurred_at"])]

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValueError("Audit events are append-only")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Audit events are append-only")
