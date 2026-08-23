from django.contrib import admin

from audit.admin_actions import AdminRoleRequiredMixin
from .models import Customer, Product


@admin.register(Customer)
class CustomerAdmin(AdminRoleRequiredMixin, admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "is_active", "created_by", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("id", "version", "created_by", "created_at", "updated_at")
    exclude = ("identity_document_hash",)


@admin.register(Product)
class ProductAdmin(AdminRoleRequiredMixin, admin.ModelAdmin):
    list_display = ("sku", "name", "price", "commission_amount", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("sku", "name")
    readonly_fields = ("id", "version", "created_at", "updated_at")
