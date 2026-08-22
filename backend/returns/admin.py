from django.contrib import admin

from .models import ReturnConfirmation, ReturnItem, ReturnReport


class ReadOnlyReturnAdmin(admin.ModelAdmin):
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
class ReturnReportAdmin(ReadOnlyReturnAdmin):
    list_display = ("id", "invoice", "seller", "status", "total", "commission_total", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "invoice__id", "seller__username")
    readonly_fields = [field.name for field in ReturnReport._meta.fields]
    inlines = (ReturnItemInline,)


@admin.register(ReturnConfirmation)
class ReturnConfirmationAdmin(ReadOnlyReturnAdmin):
    list_display = ("id", "return_report", "confirmed_by", "confirmed_at")
    readonly_fields = [field.name for field in ReturnConfirmation._meta.fields]
