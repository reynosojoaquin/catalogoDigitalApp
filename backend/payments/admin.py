from django.contrib import admin

from .models import CommissionMovement, PaymentConfirmation, PaymentReport


class ReadOnlyFinancialAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PaymentReport)
class PaymentReportAdmin(ReadOnlyFinancialAdmin):
    list_display = ("id", "invoice", "seller", "method", "amount", "status", "created_at")
    list_filter = ("method", "status")
    search_fields = ("id", "invoice__id", "seller__username", "external_terminal_reference")
    readonly_fields = [field.name for field in PaymentReport._meta.fields]


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
