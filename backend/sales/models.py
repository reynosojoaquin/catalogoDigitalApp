import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import Device
from catalog.models import Customer, Product


class Order(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", _("Submitted")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    idempotency_key = models.UUIDField(unique=True)
    request_hash = models.CharField(max_length=64)
    version = models.PositiveBigIntegerField(default=1)
    client_created_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=Q(total__gte=0), name="order_total_nonnegative"),
        ]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    product_sku = models.CharField(max_length=60)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_commission = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="unique_product_per_order"),
            models.CheckConstraint(condition=Q(quantity__gt=0), name="order_item_quantity_positive"),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name="order_item_price_nonnegative"),
            models.CheckConstraint(
                condition=Q(unit_commission__gte=0), name="order_item_commission_nonnegative"
            ),
            models.CheckConstraint(condition=Q(line_total__gte=0), name="order_item_total_nonnegative"),
        ]

    def __str__(self):
        return f"{self.order_id}:{self.product_sku}"
