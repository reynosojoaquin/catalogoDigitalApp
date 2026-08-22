import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import Device
from fulfillment.models import Invoice, InvoiceItem


class PaymentReport(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", _("Cash")
        EXTERNAL_CARD_TERMINAL = "external_card_terminal", _("External card terminal")

    class Status(models.TextChoices):
        REPORTED = "reported", _("Reported")
        CONFIRMED = "confirmed", _("Confirmed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT, related_name="payment_report")
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payment_reports",
    )
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="payment_reports")
    method = models.CharField(max_length=30, choices=Method.choices)
    external_terminal_reference = models.CharField(max_length=120, null=True, blank=True, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REPORTED, db_index=True)
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    version = models.PositiveBigIntegerField(default=1)
    client_reported_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)


class PaymentConfirmation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_report = models.OneToOneField(
        PaymentReport,
        on_delete=models.PROTECT,
        related_name="confirmation",
    )
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payment_confirmations",
    )
    confirmed_at = models.DateTimeField()
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CommissionMovement(models.Model):
    class MovementType(models.TextChoices):
        CREDIT = "credit", _("Credit")
        DEBIT = "debit", _("Debit")

    class Status(models.TextChoices):
        AVAILABLE = "available", _("Available")
        SETTLED = "settled", _("Settled")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="commission_movements",
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="commission_movements")
    invoice_item = models.ForeignKey(
        InvoiceItem,
        on_delete=models.PROTECT,
        related_name="commission_movements",
    )
    payment_confirmation = models.ForeignKey(
        PaymentConfirmation,
        on_delete=models.PROTECT,
        related_name="commission_movements",
    )
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["invoice_item"],
                condition=Q(movement_type="credit"),
                name="unique_commission_credit_per_invoice_item",
            ),
        ]

    def __str__(self):
        return str(self.id)
