import uuid

from django.conf import settings
from django.db import models

from accounts.models import Device


class SyncChange(models.Model):
    sequence = models.BigAutoField(primary_key=True)
    entity_type = models.CharField(max_length=30)
    entity_id = models.UUIDField()
    version = models.PositiveBigIntegerField()
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sequence"]
        constraints = [models.UniqueConstraint(
            fields=["entity_type", "entity_id", "version"], name="unique_sync_entity_version"
        )]


class SyncOperationReceipt(models.Model):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        CONFLICT = "conflict", "Conflict"
        REJECTED = "rejected", "Rejected"

    operation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sync_receipts")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="sync_receipts")
    entity_type = models.CharField(max_length=30)
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    client_timestamp = models.DateTimeField()
    client_version = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, db_index=True)
    entity_id = models.UUIDField(null=True, blank=True)
    conflict_code = models.CharField(max_length=50, blank=True)
    server_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-server_timestamp"]


class SyncDeviceCursor(models.Model):
    device = models.OneToOneField(Device, on_delete=models.PROTECT, related_name="sync_cursor")
    last_sequence = models.PositiveBigIntegerField(default=0)
    acknowledged_at = models.DateTimeField(auto_now=True)
