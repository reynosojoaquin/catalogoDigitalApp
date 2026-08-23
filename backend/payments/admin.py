from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from audit.admin_actions import AdminRoleRequiredMixin, DomainActionAdminMixin
from .services import PaymentIdempotencyConflictError, PaymentNotConfirmableError, confirm_payment
from .models import CommissionMovement, PaymentConfirmation, PaymentReport


class ReadOnlyFinancialAdmin(AdminRoleRequiredMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PaymentReport)
class PaymentReportAdmin(DomainActionAdminMixin, ReadOnlyFinancialAdmin):
    list_display = ("id", "invoice", "seller", "method", "amount", "status", "created_at")
    list_filter = ("method", "status")
    search_fields = ("id", "invoice__id", "seller__username", "external_terminal_reference")
    readonly_fields = [field.name for field in PaymentReport._meta.fields]
    actions = ("confirm_payments",)

    @admin.action(permissions=["administer"], description=_("Confirm full payment"))
    def confirm_payments(self, request, queryset):
        confirmed = 0
        skipped = 0
        for report in queryset.order_by("created_at", "id"):
            try:
                confirm_payment(
                    actor=request.user,
                    confirmation_id=uuid.uuid4(),
                    payment_report_id=report.id,
                    confirmed_at=timezone.now(),
                    idempotency_key=uuid.uuid4(),
                    correlation_id=self.correlation_id(request),
                )
                confirmed += 1
            except (PaymentIdempotencyConflictError, PaymentNotConfirmableError):
                self.audit_denied(
                    request,
                    resource_type="payment_report",
                    resource_id=report.id,
                    reason="payment_not_confirmable",
                )
                skipped += 1
        if confirmed:
            self.message_user(request, _("Confirmed payments: %(count)d") % {"count": confirmed})
        if skipped:
            self.message_user(
                request,
                _("Payments not eligible for confirmation: %(count)d") % {"count": skipped},
                level="warning",
            )


@admin.register(PaymentConfirmation)
class PaymentConfirmationAdmin(ReadOnlyFinancialAdmin):
    list_display = ("id", "payment_report", "confirmed_by", "confirmed_at", "created_at")
    search_fields = ("id", "payment_report__id", "confirmed_by__username")
    readonly_fields = [field.name for field in PaymentConfirmation._meta.fields]


@admin.register(CommissionMovement)
class CommissionMovementAdmin(ReadOnlyFinancialAdmin):
    list_display = ("id", "seller", "invoice", "movement_type", "amount", "status", "created_at")
    list_filter = ("movement_type", "status")
    search_fields = ("id", "invoice__id", "seller__username")
    readonly_fields = [field.name for field in CommissionMovement._meta.fields]
