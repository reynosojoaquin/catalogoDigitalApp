from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from audit.admin_actions import AdminRoleRequiredMixin, DomainActionAdminMixin
from .models import ReturnConfirmation, ReturnItem, ReturnReport
from .services import ReturnConflictError, confirm_return


class ReadOnlyReturnAdmin(AdminRoleRequiredMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in ReturnItem._meta.fields]


@admin.register(ReturnReport)
class ReturnReportAdmin(DomainActionAdminMixin, ReadOnlyReturnAdmin):
    list_display = ("id", "invoice", "seller", "status", "total", "commission_total", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "invoice__id", "seller__username")
    readonly_fields = [field.name for field in ReturnReport._meta.fields]
    inlines = (ReturnItemInline,)
    actions = ("confirm_returns",)

    @admin.action(permissions=["administer"], description=_("Confirm return"))
    def confirm_returns(self, request, queryset):
        confirmed = 0
        skipped = 0
        for report in queryset.order_by("created_at", "id"):
            try:
                confirm_return(
                    actor=request.user,
                    confirmation_id=uuid.uuid4(),
                    return_report_id=report.id,
                    confirmed_at=timezone.now(),
                    idempotency_key=uuid.uuid4(),
                    correlation_id=self.correlation_id(request),
                )
                confirmed += 1
            except ReturnConflictError:
                skipped += 1
        if confirmed:
            self.message_user(request, _("Confirmed returns: %(count)d") % {"count": confirmed})
        if skipped:
            self.message_user(
                request,
                _("Returns not eligible for confirmation: %(count)d") % {"count": skipped},
                level="warning",
            )


@admin.register(ReturnConfirmation)
class ReturnConfirmationAdmin(ReadOnlyReturnAdmin):
    list_display = ("id", "return_report", "confirmed_by", "confirmed_at")
    readonly_fields = [field.name for field in ReturnConfirmation._meta.fields]
