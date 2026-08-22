import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from sales.models import Order, OrderItem


class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="delivery")
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="confirmed_deliveries",
    )
    delivered_at = models.DateTimeField()
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = "unpaid", _("Unpaid")
        PAID = "paid", _("Paid")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery = models.OneToOneField(Delivery, on_delete=models.PROTECT, related_name="invoice")
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="invoice")
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    customer_id_snapshot = models.UUIDField()
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID, db_index=True)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    version = models.PositiveBigIntegerField(default=1)
    issued_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-issued_at"]
        constraints = [
            models.CheckConstraint(condition=Q(total__gte=0), name="invoice_total_nonnegative"),
        ]

    def __str__(self):
        return str(self.id)


class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="items")
    order_item = models.OneToOneField(OrderItem, on_delete=models.PROTECT, related_name="invoice_item")
    product_id_snapshot = models.UUIDField()
    product_sku = models.CharField(max_length=60)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_commission = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name="invoice_item_quantity_positive"),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name="invoice_item_price_nonnegative"),
            models.CheckConstraint(
                condition=Q(unit_commission__gte=0), name="invoice_item_commission_nonnegative"
            ),
            models.CheckConstraint(condition=Q(line_total__gte=0), name="invoice_item_total_nonnegative"),
        ]

    def __str__(self):
        return f"{self.invoice_id}:{self.product_sku}"
