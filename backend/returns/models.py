import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import Device
from fulfillment.models import Invoice, InvoiceItem


class ReturnReport(models.Model):
    class Status(models.TextChoices):
        REPORTED = "reported", _("Reported")
        CONFIRMED = "confirmed", _("Confirmed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="return_reports")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="return_reports")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="return_reports")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REPORTED, db_index=True)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    commission_total = models.DecimalField(max_digits=14, decimal_places=2)
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    version = models.PositiveBigIntegerField(default=1)
    client_reported_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=Q(total__gte=0), name="return_total_nonnegative"),
            models.CheckConstraint(
                condition=Q(commission_total__gte=0), name="return_commission_nonnegative"
            ),
        ]


class ReturnItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_report = models.ForeignKey(ReturnReport, on_delete=models.PROTECT, related_name="items")
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.PROTECT, related_name="return_items")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_commission = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2)
    commission_total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["return_report", "invoice_item"], name="unique_invoice_item_per_return"
            ),
            models.CheckConstraint(condition=Q(quantity__gt=0), name="return_item_quantity_positive"),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name="return_item_price_nonnegative"),
            models.CheckConstraint(
                condition=Q(unit_commission__gte=0), name="return_item_commission_nonnegative"
            ),
            models.CheckConstraint(condition=Q(line_total__gte=0), name="return_item_total_nonnegative"),
            models.CheckConstraint(
                condition=Q(commission_total__gte=0), name="return_item_commission_total_nonnegative"
            ),
        ]


class ReturnConfirmation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_report = models.OneToOneField(ReturnReport, on_delete=models.PROTECT, related_name="confirmation")
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="return_confirmations"
    )
    confirmed_at = models.DateTimeField()
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
