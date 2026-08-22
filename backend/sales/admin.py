from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from audit.admin_actions import DomainActionAdminMixin
from fulfillment.services import (
    DeliveryIdempotencyConflictError,
    OrderNotDeliverableError,
    confirm_complete_delivery,
)
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in OrderItem._meta.fields]


@admin.register(Order)
class OrderAdmin(DomainActionAdminMixin, admin.ModelAdmin):
    list_display = ("id", "seller", "customer", "status", "total", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "seller__username", "customer__full_name")
    readonly_fields = [field.name for field in Order._meta.fields]
    inlines = (OrderItemInline,)
    actions = ("confirm_deliveries",)

    @admin.action(permissions=["administer"], description=_("Confirm complete delivery"))
    def confirm_deliveries(self, request, queryset):
        completed = 0
        skipped = 0
        for order in queryset.order_by("created_at", "id"):
            try:
                confirm_complete_delivery(
                    actor=request.user,
                    delivery_id=uuid.uuid4(),
                    order_id=order.id,
                    delivered_at=timezone.now(),
                    idempotency_key=uuid.uuid4(),
                    correlation_id=self.correlation_id(request),
                )
                completed += 1
            except (DeliveryIdempotencyConflictError, OrderNotDeliverableError):
                skipped += 1
        if completed:
            self.message_user(request, _("Completed deliveries: %(count)d") % {"count": completed})
        if skipped:
            self.message_user(
                request,
                _("Orders not eligible for delivery: %(count)d") % {"count": skipped},
                level="warning",
            )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
