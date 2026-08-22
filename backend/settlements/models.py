import uuid

from django.conf import settings
from django.db import models

from payments.models import CommissionMovement


class CommissionSettlement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="commission_settlements",
    )
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="confirmed_commission_settlements",
    )
    period_ends_at = models.DateTimeField()
    total = models.DecimalField(max_digits=14, decimal_places=2)
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    confirmed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-confirmed_at"]

    def __str__(self):
        return str(self.id)


class CommissionSettlementItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    settlement = models.ForeignKey(
        CommissionSettlement,
        on_delete=models.PROTECT,
        related_name="items",
    )
    movement = models.OneToOneField(
        CommissionMovement,
        on_delete=models.PROTECT,
        related_name="settlement_item",
    )
    movement_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    signed_amount = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        ordering = ["id"]
