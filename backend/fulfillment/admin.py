from django.contrib import admin

from .models import Delivery, Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in InvoiceItem._meta.fields]


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "confirmed_by", "delivered_at", "created_at")
    readonly_fields = [field.name for field in Delivery._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "seller", "customer_name", "status", "total", "issued_at")
    list_filter = ("status",)
    search_fields = ("id", "order__id", "seller__username", "customer_name")
    readonly_fields = [field.name for field in Invoice._meta.fields]
    inlines = (InvoiceItemInline,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
