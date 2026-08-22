from django.contrib import admin

from .models import SyncChange, SyncDeviceCursor, SyncOperationReceipt


class ReadOnlySyncAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SyncChange)
class SyncChangeAdmin(ReadOnlySyncAdmin):
    list_display = ("sequence", "entity_type", "entity_id", "version", "occurred_at")
    list_filter = ("entity_type",)
    search_fields = ("entity_id",)


@admin.register(SyncOperationReceipt)
class SyncOperationReceiptAdmin(ReadOnlySyncAdmin):
    list_display = ("operation_id", "seller", "device", "entity_type", "status", "server_timestamp")
    list_filter = ("entity_type", "status")
    search_fields = ("operation_id", "entity_id", "seller__username")


@admin.register(SyncDeviceCursor)
class SyncDeviceCursorAdmin(ReadOnlySyncAdmin):
    list_display = ("device", "last_sequence", "acknowledged_at")
