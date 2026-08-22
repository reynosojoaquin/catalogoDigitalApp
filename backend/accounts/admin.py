from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from audit.admin_actions import DomainActionAdminMixin
from settlements.services import SettlementConflictError, confirm_settlement
from .models import Device, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(DomainActionAdminMixin, admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")
    actions = ("settle_available_commissions",)

    @admin.action(permissions=["administer"], description=_("Settle available commissions"))
    def settle_available_commissions(self, request, queryset):
        settled = 0
        skipped = 0
        timestamp = timezone.now()
        for profile in queryset.select_related("user").order_by("user_id"):
            if profile.role != UserProfile.Role.SELLER:
                skipped += 1
                continue
            try:
                confirm_settlement(
                    actor=request.user,
                    settlement_id=uuid.uuid4(),
                    seller_id=profile.user_id,
                    period_ends_at=timestamp,
                    confirmed_at=timestamp,
                    idempotency_key=uuid.uuid4(),
                    correlation_id=self.correlation_id(request),
                )
                settled += 1
            except SettlementConflictError:
                skipped += 1
        if settled:
            self.message_user(request, _("Commission settlements created: %(count)d") % {"count": settled})
        if skipped:
            self.message_user(
                request,
                _("Profiles without settleable commissions: %(count)d") % {"count": skipped},
                level="warning",
            )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "platform", "app_version", "is_active", "last_seen_at")
    list_filter = ("platform", "is_active")
    search_fields = ("id", "user__username")
    readonly_fields = ("id", "registered_at", "last_seen_at")
