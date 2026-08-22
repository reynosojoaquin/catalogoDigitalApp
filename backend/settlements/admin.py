from django.contrib import admin

from .models import CommissionSettlement, CommissionSettlementItem


class SettlementItemInline(admin.TabularInline):
    model = CommissionSettlementItem
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in CommissionSettlementItem._meta.fields]


@admin.register(CommissionSettlement)
class CommissionSettlementAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "total", "period_ends_at", "confirmed_by", "confirmed_at")
    search_fields = ("id", "seller__username")
    readonly_fields = [field.name for field in CommissionSettlement._meta.fields]
    inlines = (SettlementItemInline,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
